import sys
import logging
from .config import settings

def setup_logger(name: str):
    """配置带格式的日志输出"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # 使用直观的格式：时间 - 名称 - 等级 - 消息
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# 预置常用业务 logger
logger = setup_logger("AI-System")
agent_logger = setup_logger("🤖-Agent")
tool_logger = setup_logger("⚙️-Tool")
rag_logger = setup_logger("🧠-RAG")
