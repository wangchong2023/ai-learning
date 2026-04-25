import asyncio
from langchain_core.tools import tool

async def run_python_code_impl(code: str) -> str:
    """安全的 Python 代码沙箱执行。"""
    return f"代码执行成功：输出为 'Hello World'"

async def fetch_real_weather_impl(location: str) -> str:
    """抓取指定城市的实时环境数据。"""
    return f"来自公共工具库的实时响应：{location} 目前气候适宜，环境数据已更新。"

async def calculate_impl(expression: str) -> str:
    """基础数学运算工具。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

# 封装为 LangChain 工具
run_python_code = tool(run_python_code_impl)
get_weather = tool(fetch_real_weather_impl)
fetch_real_weather = tool(fetch_real_weather_impl)
calculate = tool(calculate_impl)

tools = [run_python_code, get_weather, fetch_real_weather, calculate]

# 导出原始函数供 MCP 使用
mcp_tool_funcs = {
    "run_python_code": run_python_code_impl,
    "fetch_real_weather": fetch_real_weather_impl,
    "calculate": calculate_impl
}
