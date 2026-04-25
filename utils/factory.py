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
    
    # 恢复用户要求的详细获取说明
    rag_logger.info(f"🧠 正在加载嵌入模型: {settings.EMBEDDING_MODEL}")
    rag_logger.info("📢 [提示] 系统正在从 Hugging Face 开源社区获取模型权重 (若本地已有缓存则直接从 ~/.cache 加载)。")
    rag_logger.info("🚀 正在将权重加载至本地内存以进行语义计算...")
    
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
