import os
from pathlib import Path
from dotenv import load_dotenv

# 定位项目根目录 (现移至 source/ 下)
PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT.parent / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

class Settings:
    """全局项目配置"""
    
    # API 密钥与端点
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com"
    
    # ==========================================
    # LangSmith 可观测性配置
    # ==========================================
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "AI-Learning-Lab")

    # 自动设置环境变量以启用追踪
    if LANGSMITH_TRACING and LANGSMITH_API_KEY:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
    
    # 模型选型
    LLM_MODEL = "deepseek-chat"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG 配置
    CHROMA_PERSIST_DIR = PROJECT_ROOT / "apps" / "rag_app" / "vector_storage" / "chroma_db"
    CHUNK_SIZE = 300
    CHUNK_OVERLAP = 30
    RETRIEVER_K = 5
    
    # 状态机持久化配置
    SQLITE_DB_PATH = ":memory:"
    
    # 日志等级
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
