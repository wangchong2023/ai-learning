import os
import shutil
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

# 引入基础设施
from utils.config import settings
from utils.logger import rag_logger

SOURCE_DATA_DIR = Path(__file__).parent / "source_data"

def init_llm():
    return ChatOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        model=settings.LLM_MODEL,
        temperature=0
    )

def init_embeddings():
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    rag_logger.info(f"正在准备本地嵌入模型: {settings.EMBEDDING_MODEL}")
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

class ModernHybridRetriever(BaseRetriever):
    vector_retriever: Any
    bm25_retriever: Any

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        v_docs = self.vector_retriever.invoke(query)
        b_docs = self.bm25_retriever.invoke(query)
        all_docs = {d.page_content: d for d in (v_docs + b_docs)}
        rag_logger.info(f"检索完成，合并后共 {len(all_docs)} 个片段")
        return list(all_docs.values())

async def get_dynamic_context(query: str, llm: ChatOpenAI) -> Dict[str, str]:
    context_data = {"weather": "无需实时数据"}
    if any(k in query for k in ["天气", "温度"]):
        rag_logger.info("检测到天气意图，触发外部工具增强...")
        from tools.common_tools import fetch_real_weather_impl
        # 简单提取前两个字作为城市模拟
        city = query[:2] if len(query) >= 2 else "北京"
        context_data["weather"] = await fetch_real_weather_impl(city)
    return context_data

async def main():
    rag_logger.info("🚀 RAG 应用启动 (工程优化版)")
    llm = init_llm()
    embeddings = init_embeddings()
    
    # 模拟数据准备
    if not SOURCE_DATA_DIR.exists(): SOURCE_DATA_DIR.mkdir()
    (SOURCE_DATA_DIR / "knowledge.txt").write_text("本项目基于 LangChain 0.3 构建，展示了混合检索的威力。", encoding="utf-8")
    
    loader = TextLoader(str(SOURCE_DATA_DIR / "knowledge.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    splits = splitter.split_documents(docs)
    
    if settings.CHROMA_PERSIST_DIR.exists(): shutil.rmtree(settings.CHROMA_PERSIST_DIR)
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=str(settings.CHROMA_PERSIST_DIR))
    
    hybrid_retriever = ModernHybridRetriever(
        vector_retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        bm25_retriever=BM25Retriever.from_documents(splits, k=3)
    )
    
    rag_logger.info("✅ 引擎就绪。")

    while True:
        query = input("\n[问题]: ")
        if query.lower() in ['quit', 'exit']: break
        
        raw_docs = hybrid_retriever.invoke(query)
        external_info = await get_dynamic_context(query, llm)
        
        final_prompt = ChatPromptTemplate.from_template("上下文: {context}\n补充: {weather}\n问题: {question}")
        chain = final_prompt | llm | StrOutputParser()
        
        result = await chain.ainvoke({
            "context": "\n".join([d.page_content for d in raw_docs]),
            "weather": external_info["weather"],
            "question": query
        })
        print(f"💬 [回答]:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
