import sys
import os
import logging
from .config import settings, PROJECT_ROOT

def setup_logger(name: str):
    """配置带格式的日志输出"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    if not logger.handlers:
        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        
        # 文件持久化输出 (工业级必备)
        log_dir = PROJECT_ROOT.parent / "logs"
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "ai-system.log", encoding="utf-8")
        
        # 使用直观的格式：时间 - 名称 - 等级 - 消息
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# 预置常用业务 logger
logger = setup_logger("AI-System")
agent_logger = setup_logger("🤖-Agent")
tool_logger = setup_logger("⚙️-Tool")
rag_logger = setup_logger("🧠-RAG")
