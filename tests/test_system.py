import asyncio
import unittest
from utils.config import settings
from utils.logger import logger
from tools.common_tools import calculate_impl, fetch_real_weather_impl

class TestAISystem(unittest.IsolatedAsyncioTestCase):
    """项目核心功能集成测试"""

    def test_config_loading(self):
        """验证配置是否正确加载"""
        logger.info("正在测试配置加载...")
        self.assertIsNotNone(settings.DEEPSEEK_API_KEY, "API Key 未能从环境变量加载")
        self.assertTrue(settings.LLM_MODEL.startswith("deepseek"), "默认模型配置错误")

    async def test_math_tool(self):
        """验证数学工具逻辑"""
        logger.info("正在测试数学工具...")
        result = await calculate_impl("100 + 200")
        self.assertIn("300", result)

    async def test_weather_tool(self):
        """验证天气工具模拟逻辑"""
        logger.info("正在测试天气工具...")
        result = await fetch_real_weather_impl("北京")
        self.assertIn("晴朗", result)

if __name__ == "__main__":
    unittest.main()
