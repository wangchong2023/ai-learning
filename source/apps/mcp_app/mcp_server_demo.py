from mcp.server.fastmcp import FastMCP

# 创建一个演示用的 FastMCP 服务端
# 它展示了如何独立于项目主工具库创建一个微服务
mcp = FastMCP("Weather-Demo-Service")

@mcp.tool()
async def get_demo_weather(city: str) -> str:
    """获取演示环境下的天气。"""
    return f"{city} 演示天气：15°C, 阴天。"

if __name__ == "__main__":
    # 使用 stdio 传输协议启动
    mcp.run(transport='stdio')
