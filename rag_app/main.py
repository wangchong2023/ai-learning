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
    print(f"🧠 正在加载嵌入模型: {RAG_CONFIG['embedding_model']}")
    print("📢 [提示] 模型正在从 Hugging Face 开源社区获取 (若本地已有缓存则直接加载)。")
    return HuggingFaceEmbeddings(
        model_name=RAG_CONFIG["embedding_model"],
        show_progress=False
    )

from typing import List, Dict, Any, Optional
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun

# ... (保持 imports 之前的配置)

class ModernHybridRetriever(BaseRetriever):
    """
    一个集成了向量搜索和关键词搜索的现代化混合检索器。
    
    Attributes:
        vector_retriever: 负责语义检索的向量库检索器。
        bm25_retriever: 负责精确关键词匹配的检索器。
    """
    vector_retriever: Any
    bm25_retriever: Any

    def _get_relevant_documents(
        self, query: str, *, run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        """
        执行混合检索并合并结果。
        """
        v_docs = self.vector_retriever.invoke(query)
        b_docs = self.bm25_retriever.invoke(query)
        
        # 使用内容作为 Key 进行合并去重
        all_docs = {d.page_content: d for d in (v_docs + b_docs)}
        return list(all_docs.values())

async def get_dynamic_context(query: str, llm: ChatOpenAI) -> Dict[str, str]:
    """
    根据用户查询动态决定是否增强外部实时上下文。
    
    Args:
        query: 用户输入的原始问题。
        llm: 用于潜在意图识别的大模型实例。
        
    Returns:
        Dict[str, str]: 包含外部补充信息的字典。
    """
    context_data = {"weather": "无需实时天气数据"}
    
    # 意图检测逻辑
    if any(keyword in query for keyword in ["天气", "温度", "气候"]):
        # 尝试提取地理位置
        for city in ["北京", "上海", "南京", "广州", "深圳", "南京"]:
            if city in query:
                from tools.common_tools import fetch_real_weather_impl
                context_data["weather"] = await fetch_real_weather_impl(city)
                break
    return context_data

def create_knowledge_files() -> List[Path]:
    """
    自动构建项目内置的知识库模拟文件。
    
    Returns:
        List[Path]: 生成的文件路径列表。
    """
    if not SOURCE_DATA_DIR.exists():
        SOURCE_DATA_DIR.mkdir(parents=True)
    
    docs = {
        "langchain_info.txt": "LangChain 是一个构建大模型应用的框架，由 Harrison Chase 于 2022 年创建。其核心组件包括 Chain、Memory 和 Agent。",
        "vector_db_info.txt": "向量数据库（如 Chroma）通过向量嵌入来存储非结构化数据。它支持高效的语义检索，而非简单的关键词匹配。",
        "rag_concepts.txt": "RAG (检索增强生成) 结合了检索系统和生成模型，能有效减少模型的幻觉问题并提供实时知识。"
    }
    
    file_paths = []
    for name, content in docs.items():
        p = SOURCE_DATA_DIR / name
        p.write_text(content, encoding="utf-8")
        file_paths.append(p)
    return file_paths

async def main():
    """RAG 应用主循环"""
    print("🌟 现代化交互式 RAG (V3 规范版) 启动...")
    llm = init_llm()
    embeddings = init_embeddings()
    
    # 1. 数据准备
    files = create_knowledge_files()
    all_docs = []
    for p in files:
        loader = TextLoader(str(p), encoding="utf-8")
        all_docs.extend(loader.load())
    
    # 2. 切分与索引
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=RAG_CONFIG["chunk_size"], 
        chunk_overlap=RAG_CONFIG["chunk_overlap"]
    )
    splits = splitter.split_documents(all_docs)
    
    if CHROMA_DB_PATH.exists(): shutil.rmtree(CHROMA_DB_PATH)
    vectorstore = Chroma.from_documents(splits, embeddings, persist_directory=str(CHROMA_DB_PATH))
    
    # 3. 构造标准混合检索器
    hybrid_retriever = ModernHybridRetriever(
        vector_retriever=vectorstore.as_retriever(search_kwargs={"k": RAG_CONFIG["top_k"]}),
        bm25_retriever=BM25Retriever.from_documents(splits, k=RAG_CONFIG["top_k"])
    )
    
    print("✅ RAG 引擎就绪。输入 'quit' 退出。")

    while True:
        try:
            query = input("\n[问题]: ")
            if query.lower() in ['quit', 'exit']: break
            if not query.strip(): continue

            # 执行混合检索
            raw_docs = hybrid_retriever.invoke(query)
            
            # 获取动态外部信息
            external_info = await get_dynamic_context(query, llm)
            
            # 推理合成
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
            print(f"❌ 系统运行异常: {e}")

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
