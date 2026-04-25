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
    rag_logger.info(f"🎨 从工厂初始化嵌入模型: {settings.EMBEDDING_MODEL}")
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
