# MCP (Model Context Protocol) 演示

本模块演示了 Anthropic 推出的最新模型上下文协议。

## 📂 结构说明
*   `mcp_server_demo.py`：一个轻量级的 MCP 服务端示例。
*   `mcp_client_demo.py`：演示如何连接服务端并发现/调用远程工具。

## 💡 与项目集成的区别
*   **本目录示例**：是自包含的、用于理解协议的 Demo。
*   **全局生产服务**：位于根目录 `tools/mcp_server.py`，它将整个项目的生产级工具库一键发布。

## 🚀 运行 Demo
```bash
# 在两个终端分别尝试或直接运行 client
./env/venv/bin/python3 mcp_app/mcp_client_demo.py
```
