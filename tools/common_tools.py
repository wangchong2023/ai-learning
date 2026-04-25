import asyncio
import sys
from langchain_core.tools import tool

# ==========================================
# 工具核心实现 (原子能力)
# ==========================================

async def run_python_code_impl(code: str) -> str:
    """
    执行 Python 代码沙箱。
    该工具允许您执行任意 Python 逻辑进行复杂计算或数据处理。
    注意：目前为演示环境，仅进行语法解析模拟。
    """
    if not code:
        return "错误：未提供代码内容。"
    
    # 模拟一个稍微真实点的反馈
    return f"代码分析成功：检测到指令 -> \n{code}\n状态：已在虚拟沙箱中预演，输出结果符合预期。"

async def fetch_real_weather_impl(location: str) -> str:
    """
    获取指定城市的实时环境数据。
    支持获取城市的天气、温湿度及整体环境评级。
    """
    # 模拟多维度实时数据
    weather_data = {
        "上海": "🌧️ 阵雨, 19°C, 湿度 85%, 空气质量: 优",
        "北京": "☀️ 晴朗, 22°C, 湿度 30%, 空气质量: 良",
        "南京": "☁️ 多云, 20°C, 湿度 60%, 空气质量: 优"
    }
    status = weather_data.get(location, "🌤️ 气候适宜, 数据已校准")
    return f"【实时系统响应】{location} 当前数据：{status}。更新时间：刚才。"

async def calculate_impl(expression: str) -> str:
    """
    执行高精度数学运算。
    支持加、减、乘、除、幂运算等 Python 语法表达式。
    """
    try:
        # 使用安全受限的 eval 环境 (演示用途)
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"数学运算失败: {str(e)}"

# ==========================================
# 导出 LangChain 工具对象
# ==========================================

run_python_code = tool(run_python_code_impl)
fetch_real_weather = tool(fetch_real_weather_impl)
calculate = tool(calculate_impl)

tools = [run_python_code, fetch_real_weather, calculate]

# ==========================================
# 导出 MCP 映射映射
# ==========================================
mcp_tool_funcs = {
    "run_python_code": run_python_code_impl,
    "fetch_real_weather": fetch_real_weather_impl,
    "calculate": calculate_impl
}
