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
    """
    重排序组件：负责从初筛结果中选出最相关的上下文。
    工业界通常使用 Cross-Encoder (如 BGE-Reranker)。此处实现逻辑骨架。
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    async def rerank(self, query: str, documents: List[Document]) -> List[Document]:
        """对文档进行评分并排序 (本处演示逻辑：保持原始顺序，但在生产中可接入专门模型)"""
        rag_logger.info(f"正在对 {len(documents)} 个候选文档进行重排序过滤...")
        # 实际生产中这里会调用 Cross-Encoder 模型进行精排打分
        # 暂时返回前两个最相关的
        return documents[:2]

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
    rag_logger.info("🚀 RAG 应用启动 (V4 工业级架构版)")
    llm = create_llm()
    embeddings = create_embeddings()
    reranker = ModernReranker(llm)
    
    if not SOURCE_DATA_DIR.exists(): SOURCE_DATA_DIR.mkdir()
    (SOURCE_DATA_DIR / "knowledge.txt").write_text("RAG 架构通常包含召回(Recall)与重排(Rerank)两个阶段。", encoding="utf-8")
    
    loader = TextLoader(str(SOURCE_DATA_DIR / "knowledge.txt"), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    splits = splitter.split_documents(docs)
    
    if settings.CHROMA_PERSIST_DIR.exists(): shutil.rmtree(settings.CHROMA_PERSIST_DIR)
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=str(settings.CHROMA_PERSIST_DIR))
    
    hybrid_retriever = ModernHybridRetriever(
        vector_retriever=vectorstore.as_retriever(search_kwargs={"k": 5}), # 召回阶段多拿一些 (Top-5)
        bm25_retriever=BM25Retriever.from_documents(splits, k=5)
    )
    
    rag_logger.info("✅ RAG 引擎就绪。输入 'quit' 退出。")

    while True:
        try:
            query = input("\n[问题]: ")
            if query.lower() in ['quit', 'exit']: break
            if not query.strip(): continue
            
            # 1. 混合检索 (召回)
            candidates = hybrid_retriever.invoke(query)
            
            # 2. 深度精排 (重排序)
            top_docs = await reranker.rerank(query, candidates)
            
            # 3. 动态获取外部信息
            external_info = await get_dynamic_context(query, llm)
            
            # 4. 推理合成
            final_prompt = ChatPromptTemplate.from_template("""
你是一个精通 RAG 架构的专家。请基于以下精排后的上下文回答问题。
[精排上下文]: {context}
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
        except Exception as e:
            rag_logger.error(f"运行出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())
