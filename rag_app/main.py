import os
import shutil
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"
CHROMA_DB_PATH = SCRIPT_DIR / "vector_storage" / "chroma_db"
SOURCE_DATA_DIR = SCRIPT_DIR / "source_data"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

def init_llm():
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        temperature=0
    )

def init_embeddings():
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    print("🧠 正在初始化本地嵌入模型...")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        show_progress=False
    )

class ModernHybridRetriever:
    def __init__(self, vectorstore, documents):
        self.vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 2

    def invoke(self, query: str):
        v_docs = self.vector_retriever.invoke(query)
        b_docs = self.bm25_retriever.invoke(query)
        all_docs = {d.page_content: d for d in (v_docs + b_docs)}
        return list(all_docs.values())

async def compress_documents(docs: list[Document], query: str, llm: ChatOpenAI):
    if not docs: return "暂无相关参考文档。"
    compress_prompt = ChatPromptTemplate.from_template(
        "以下文档内容中提取与问题 '{query}' 相关的信息：\n{context}"
    )
    context = "\n---\n".join([d.page_content for d in docs])
    chain = compress_prompt | llm | StrOutputParser()
    return await chain.ainvoke({"context": context, "query": query})

async def main():
    print("🌟 现代化交互式 RAG 演示启动...")
    llm = init_llm()
    embeddings = init_embeddings()
    
    if not SOURCE_DATA_DIR.exists(): SOURCE_DATA_DIR.mkdir(parents=True)
    (SOURCE_DATA_DIR / "knowledge.txt").write_text("LangChain 是 AI 应用开发框架。", encoding="utf-8")

    all_docs = []
    for p in SOURCE_DATA_DIR.glob("*.txt"):
        loader = TextLoader(str(p), encoding="utf-8")
        all_docs.extend(loader.load())
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    splits = splitter.split_documents(all_docs)
    
    if CHROMA_DB_PATH.exists(): shutil.rmtree(CHROMA_DB_PATH)
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=str(CHROMA_DB_PATH))
    hybrid_retriever = ModernHybridRetriever(vectorstore, splits)
    
    while True:
        try:
            query = input("\n[问题]: ")
            if query.lower() in ['quit', 'exit']: break
            raw_docs = hybrid_retriever.invoke(query)
            compressed_context = await compress_documents(raw_docs, query, llm)
            from tools.common_tools import fetch_real_weather_impl
            weather = await fetch_real_weather_impl("北京")
            
            final_prompt = ChatPromptTemplate.from_template("结合知识回答: {context}\n实时: {weather}\n问: {question}")
            chain = final_prompt | llm | StrOutputParser()
            result = await chain.ainvoke({"context": compressed_context, "weather": weather, "question": query})
            print(f"💬 [回答]:\n{result}")
        except Exception as e: print(f"❌ 出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())
