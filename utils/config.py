import os
from pathlib import Path
from dotenv import load_dotenv

# 定位项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / "env" / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

class Settings:
    """全局项目配置"""
    
    # API 密钥与端点
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com"
    
    # 模型选型
    LLM_MODEL = "deepseek-chat"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG 配置
    CHROMA_PERSIST_DIR = PROJECT_ROOT / "rag_app" / "vector_storage" / "chroma_db"
    CHUNK_SIZE = 300
    CHUNK_OVERLAP = 30
    
    # 日志等级
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
