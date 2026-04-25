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

# ==========================================
# 1. 全局配置与路径 (消除硬编码路径)
# ==========================================
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"
CHROMA_DB_PATH = SCRIPT_DIR / "vector_storage" / "chroma_db"
SOURCE_DATA_DIR = SCRIPT_DIR / "source_data"

# RAG 参数配置
RAG_CONFIG = {
    "chunk_size": 300,
    "chunk_overlap": 30,
    "top_k": 3,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
}

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

# ==========================================
# 2. 核心组件初始化
# ==========================================

def init_llm():
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        temperature=0
    )

def init_embeddings():
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    print(f"🧠 正在加载嵌入模型: {RAG_CONFIG['embedding_model']}...")
    return HuggingFaceEmbeddings(
        model_name=RAG_CONFIG["embedding_model"],
        show_progress=False
    )

class ModernHybridRetriever:
    def __init__(self, vectorstore, documents):
        self.vector_retriever = vectorstore.as_retriever(search_kwargs={"k": RAG_CONFIG["top_k"]})
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = RAG_CONFIG["top_k"]

    def invoke(self, query: str):
        v_docs = self.vector_retriever.invoke(query)
        b_docs = self.bm25_retriever.invoke(query)
        # 合并去重
        all_docs = {d.page_content: d for d in (v_docs + b_docs)}
        return list(all_docs.values())

# ==========================================
# 3. 动态工具判定 (消除逻辑硬编码)
# ==========================================

async def get_dynamic_context(query: str, llm: ChatOpenAI):
    """根据查询内容，动态决定是否调用外部工具"""
    context_data = {"weather": "无需实时天气数据"}
    
    # 简单的意图识别：如果包含“天气”关键词，则尝试提取城市并查询
    if "天气" in query:
        # 模拟 LLM 提取城市（此处简化处理）
        for city in ["北京", "上海", "南京", "广州", "深圳"]:
            if city in query:
                from tools.common_tools import fetch_real_weather_impl
                context_data["weather"] = await fetch_real_weather_impl(city)
                break
    return context_data

async def main():
    print("🌟 现代化交互式 RAG (V2 优化版) 启动...")
    llm = init_llm()
    embeddings = init_embeddings()
    
    # 初始化知识库
    from .main import create_knowledge_files # 复用之前的辅助函数
    files = create_knowledge_files()

    all_docs = []
    for p in files:
        loader = TextLoader(str(p), encoding="utf-8")
        all_docs.extend(loader.load())
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=RAG_CONFIG["chunk_size"], 
        chunk_overlap=RAG_CONFIG["chunk_overlap"]
    )
    splits = splitter.split_documents(all_docs)
    
    if CHROMA_DB_PATH.exists(): shutil.rmtree(CHROMA_DB_PATH)
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=str(CHROMA_DB_PATH))
    hybrid_retriever = ModernHybridRetriever(vectorstore, splits)
    
    print("✅ RAG 引擎就绪。")

    while True:
        try:
            query = input("\n[问题]: ")
            if query.lower() in ['quit', 'exit']: break
            if not query.strip(): continue

            # 1. 检索本地知识
            raw_docs = hybrid_retriever.invoke(query)
            
            # 2. 动态获取外部上下文 (不再硬编码北京)
            external_info = await get_dynamic_context(query, llm)
            
            # 3. 构建 Prompt
            final_prompt = ChatPromptTemplate.from_template("""
你是一个能够区分本地知识和实时数据的专家。
[本地文档参考]: {context}
[实时外部补充]: {weather}
问题: {question}
回答:""")
            
            context_str = "\n".join([d.page_content for d in raw_docs])
            chain = final_prompt | llm | StrOutputParser()
            
            result = await chain.ainvoke({
                "context": context_str,
                "weather": external_info["weather"],
                "question": query
            })
            print(f"💬 [回答]:\n{result}")
            
        except Exception as e:
            print(f"❌ 出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())
