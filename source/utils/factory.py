from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from .config import settings
from .logger import rag_logger

def create_llm(temperature: float = 0) -> ChatOpenAI:
    """统一创建配置好的 LLM 实例"""
    return ChatOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        model=settings.LLM_MODEL,
        temperature=temperature
    )

def create_embeddings() -> HuggingFaceEmbeddings:
    """统一创建配置好的 Embeddings 实例"""
    import os
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # 拟人化/业务化提示
    rag_logger.info(f"🎨 正在准备本地语义分析引擎: {settings.EMBEDDING_MODEL}")
    rag_logger.info("📢 [提示] 系统正在从 Hugging Face 获取模型知识库 (若本地已有缓存将秒速加载)。")
    rag_logger.info("🚀 知识库加载中，即将开启本地深度理解能力...")
    
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
