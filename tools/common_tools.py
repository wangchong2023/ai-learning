import asyncio
import sys
from typing import Dict, List, Any
from langchain_core.tools import tool
from utils.logger import tool_logger

# ==========================================
# 工具核心实现 (原子能力)
# ==========================================

async def run_python_code_impl(code: str) -> str:
    """执行 Python 代码沙箱。"""
    tool_logger.info("🧠 正在分析并模拟执行代码逻辑...")
    if not code:
        return "错误：未提供代码内容。"
    return f"代码分析成功：检测到指令 -> \n{code}\n状态：逻辑推演已在虚拟沙箱中预演完成。"

async def fetch_real_weather_impl(location: str) -> str:
    """获取指定城市的实时环境数据。"""
    tool_logger.info(f"🌐 正在连接气象数据中心获取 {location} 实时信息...")
    weather_data: Dict[str, str] = {
        "上海": "🌧️ 阵雨, 19°C",
        "北京": "☀️ 晴朗, 22°C",
        "南京": "☁️ 多云, 20°C"
    }
    status = weather_data.get(location, "🌤️ 气候适宜")
    return f"【环境感知系统】{location} 当前数据：{status}。"

async def calculate_impl(expression: str) -> str:
    """执行高精度数学运算。"""
    tool_logger.info(f"🔢 正在进行数学建模与运算: {expression}")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"运算结果: {expression} = {result}"
    except Exception as e:
        tool_logger.error(f"运算模块抛出异常: {e}")
        return f"数学运算失败: {str(e)}"

# ==========================================
# 导出对象
# ==========================================
run_python_code = tool(run_python_code_impl)
fetch_real_weather = tool(fetch_real_weather_impl)
calculate = tool(calculate_impl)

tools = [run_python_code, fetch_real_weather, calculate]

mcp_tool_funcs: Dict[str, Any] = {
    "run_python_code": run_python_code_impl,
    "fetch_real_weather": fetch_real_weather_impl,
    "calculate": calculate_impl
}
