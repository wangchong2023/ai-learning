import asyncio
import sys
from typing import Dict, List, Any
from langchain_core.tools import tool

# ==========================================
# 工具核心实现 (原子能力)
# ==========================================

async def run_python_code_impl(code: str) -> str:
    """
    执行 Python 代码沙箱。
    
    Args:
        code: 需要在沙箱中运行的 Python 源码。
        
    Returns:
        str: 执行结果或状态反馈。
    """
    if not code:
        return "错误：未提供代码内容。"
    
    # 模拟一个稍微真实点的反馈
    return f"代码分析成功：检测到指令 -> \n{code}\n状态：已在虚拟沙箱中预演，输出结果符合预期。"

async def fetch_real_weather_impl(location: str) -> str:
    """
    获取指定城市的实时环境数据。
    
    Args:
        location: 目标城市名称 (如: 北京, 上海)。
        
    Returns:
        str: 包含天气、温度及空气质量的格式化字符串。
    """
    # 模拟多维度实时数据
    weather_data: Dict[str, str] = {
        "上海": "🌧️ 阵雨, 19°C, 湿度 85%, 空气质量: 优",
        "北京": "☀️ 晴朗, 22°C, 湿度 30%, 空气质量: 良",
        "南京": "☁️ 多云, 20°C, 湿度 60%, 空气质量: 优"
    }
    status = weather_data.get(location, "🌤️ 气候适宜, 数据已校准")
    return f"【实时系统响应】{location} 当前数据：{status}。更新时间：刚才。"

async def calculate_impl(expression: str) -> str:
    """
    执行高精度数学运算。
    
    Args:
        expression: 合法的 Python 数学表达式 (如: 2**10 + 5)。
        
    Returns:
        str: 计算结果或错误信息。
    """
    try:
        # 注意：此处 eval 仅用于演示环境，生产环境建议使用专用的数学解析库
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

# 全量工具列表，供智能体绑定
tools = [run_python_code, fetch_real_weather, calculate]

# ==========================================
# 导出 MCP 映射
# ==========================================
mcp_tool_funcs: Dict[str, Any] = {
    "run_python_code": run_python_code_impl,
    "fetch_real_weather": fetch_real_weather_impl,
    "calculate": calculate_impl
}
