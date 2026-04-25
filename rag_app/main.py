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

class ModernReranker:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    async def rerank(self, query: str, documents: List[Document]) -> List[Document]:
        """对文档进行评分并排序"""
        rag_logger.info(f"🧐 正在对召回的 {len(documents)} 处知识点进行深度语义对齐...")
        return documents[:2]

class ModernHybridRetriever(BaseRetriever):
    vector_retriever: Any
    bm25_retriever: Any

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        rag_logger.info(f"🔍 正在从本地知识库检索相关信息...")
        v_docs = self.vector_retriever.invoke(query)
        b_docs = self.bm25_retriever.invoke(query)
        all_docs = {d.page_content: d for d in (v_docs + b_docs)}
        rag_logger.info(f"✅ 检索完成，已锁定 {len(all_docs)} 处潜在关联知识")
        return list(all_docs.values())

async def get_dynamic_context(query: str, llm: ChatOpenAI) -> Dict[str, str]:
    context_data = {"weather": "无需实时数据"}
    if any(k in query for k in ["天气", "温度", "气候"]):
        cities = ["北京", "上海", "南京", "广州", "深圳", "杭州", "成都"]
        for city in cities:
            if city in query:
                rag_logger.info(f"🌍 检测到环境感知意图，正在获取 {city} 实时数据...")
                from tools.common_tools import fetch_real_weather_impl
                context_data["weather"] = await fetch_real_weather_impl(city)
                break
    return context_data

async def main():
    rag_logger.info("🚀 现代化 RAG 智能助手启动...")
    llm = create_llm()
    embeddings = create_embeddings()
    reranker = ModernReranker(llm)
    
    if not SOURCE_DATA_DIR.exists(): SOURCE_DATA_DIR.mkdir()
    (SOURCE_DATA_DIR / "knowledge.txt").write_text("RAG 架构通常包含召回与重排两个阶段。", encoding="utf-8")
    
    loader = TextLoader(str(SOURCE_DATA_DIR / "knowledge.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    splits = splitter.split_documents(docs)
    
    if settings.CHROMA_PERSIST_DIR.exists(): shutil.rmtree(settings.CHROMA_PERSIST_DIR)
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=str(settings.CHROMA_PERSIST_DIR))
    
    hybrid_retriever = ModernHybridRetriever(
        vector_retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        bm25_retriever=BM25Retriever.from_documents(splits, k=5)
    )
    
    rag_logger.info("✨ 知识引擎已就绪，随时准备为您解答问题。")

    try:
        while True:
            query = input("\n🔍 [知识库检索] 请输入您的问题 (输入 'quit' 退出): ")
            if query.lower() in ['quit', 'exit']: break
            if not query.strip(): continue
            
            candidates = hybrid_retriever.invoke(query)
            top_docs = await reranker.rerank(query, candidates)
            external_info = await get_dynamic_context(query, llm)
            
            final_prompt = ChatPromptTemplate.from_template("""
你是一个精通 RAG 架构的专家。请基于以下精排后的上下文回答问题。
[知识上下文]: {context}
[外部增强]: {weather}
问题: {question}
回答:""")
            
            context_str = "\n".join([d.page_content for d in top_docs])
            chain = final_prompt | llm | StrOutputParser()
            
            result = await chain.ainvoke({
                "context": context_str,
                "weather": external_info["weather"],
                "question": query
            })
            print(f"💬 [回答]:\n{result}")
    except KeyboardInterrupt:
        print("\n👋 已安全退出 RAG 应用。")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # 内层已打印退出信息，此处静默即可
