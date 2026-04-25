import asyncio
from mcp.server.fastmcp import FastMCP
from .common_tools import mcp_tool_funcs

# 创建 FastMCP 实例
mcp = FastMCP("Modern-Common-Tools-Service")

# 自动注册所有公共工具
for name, func in mcp_tool_funcs.items():
    mcp.tool(name=name)(func)

if __name__ == "__main__":
    # 使用 stdio 传输协议启动服务
    mcp.run(transport='stdio')
