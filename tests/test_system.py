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

    def test_multi_agent_graph_compilation(self):
        """验证多智能体协作图是否能正确编译"""
        logger.info("正在测试多智能体架构编译...")
        from multi_agent_app.core.builder import create_multi_agent_graph
        try:
            app = create_multi_agent_graph()
            self.assertIsNotNone(app, "多智能体图编译失败")
        except Exception as e:
            self.fail(f"多智能体协作图编译抛出异常: {e}")

    def test_planner_graph_compilation(self):
        """验证 Plan-and-Execute 深度规划图是否能正确编译"""
        logger.info("正在测试深度规划架构编译...")
        from planner_app.core.builder import create_planner_graph
        try:
            app = create_planner_graph()
            self.assertIsNotNone(app, "深度规划图编译失败")
        except Exception as e:
            self.fail(f"深度规划图编译抛出异常: {e}")

if __name__ == "__main__":
    unittest.main()
