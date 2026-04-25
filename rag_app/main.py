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
from utils.factory import create_llm, create_embeddings

SOURCE_DATA_DIR = Path(__file__).parent / "source_data"

def init_llm():
    """通过工厂创建 LLM"""
    return create_llm()

def init_embeddings():
    """通过工厂创建 Embeddings"""
    return create_embeddings()

class ModernHybridRetriever(BaseRetriever):
    vector_retriever: Any
    bm25_retriever: Any

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        rag_logger.info(f"正在执行混合检索: {query}")
        v_docs = self.vector_retriever.invoke(query)
        b_docs = self.bm25_retriever.invoke(query)
        all_docs = {d.page_content: d for d in (v_docs + b_docs)}
        return list(all_docs.values())

async def get_dynamic_context(query: str, llm: ChatOpenAI) -> Dict[str, str]:
    """意图识别与动态上下文增强"""
    context_data = {"weather": "无需实时数据"}
    if any(k in query for k in ["天气", "温度", "气候"]):
        cities = ["北京", "上海", "南京", "广州", "深圳", "杭州", "成都"]
        for city in cities:
            if city in query:
                rag_logger.info(f"检测到 {city} 天气查询意图")
                from tools.common_tools import fetch_real_weather_impl
                context_data["weather"] = await fetch_real_weather_impl(city)
                break
    return context_data

async def main():
    rag_logger.info("🚀 RAG 应用启动 (V3 规范版)")
    llm = init_llm()
    embeddings = init_embeddings()
    
    # 数据持久化准备
    if not SOURCE_DATA_DIR.exists(): SOURCE_DATA_DIR.mkdir()
    (SOURCE_DATA_DIR / "knowledge.txt").write_text("本项目是 AI-Learning 的实验场。", encoding="utf-8")
    
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
    
    rag_logger.info("✅ 引擎就绪。输入 'quit' 退出。")

    while True:
        try:
            query = input("\n[问题]: ")
            if query.lower() in ['quit', 'exit']: break
            if not query.strip(): continue
            
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
        except Exception as e:
            rag_logger.error(f"运行出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())
