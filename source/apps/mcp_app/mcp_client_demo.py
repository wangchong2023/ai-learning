import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 演示如何以客户端身份连接并调用一个 MCP 服务
async def run_client_demo():
    # ⚡ 修复点：确保使用当前虚拟环境的 Python 执行器
    python_executable = sys.executable

    server_params = StdioServerParameters(
        command=python_executable,
        args=["mcp_app/mcp_server_demo.py"],
    )

    print(f"🔗 [Client]: 正在连接服务端 -> {python_executable} mcp_app/mcp_server_demo.py")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. 初始化连接
            await session.initialize()

            # 2. 列出可用工具
            tools = await session.list_tools()
            print(f"📡 [Client]: 发现远程工具 -> {[t.name for t in tools.tools]}")

            # 3. 调用工具
            result = await session.call_tool("get_demo_weather", arguments={"city": "上海"})
            print(f"⚙️ [Client]: 调用结果 -> {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_client_demo())
