# AI-Learning: 现代化 AI 应用架构实验场

本项目是一个基于 **LangChain 0.3+**、**LangGraph** 和 **MCP (Model Context Protocol)** 的全栈 AI 实验场。它展示了如何构建一个高度模块化、具备实时感知能力、且拥有人工干预机制的智能体系统。

## 🏗️ 全局架构概览

*   **能力层 (`tools/`)**：中心化工具库。采用“定义一次，多处运行”的原则，支持被 LangChain 直接调用，或通过 **MCP Server** 发布给外部客户端。
*   **编排层 (`langgraph_app/`)**：核心高级智能体。基于图的状态机架构，深度集成 **HITL (人工审批流)** 确保高危操作受控。
*   **增强层 (`rag_app/`)**：**Active RAG** 演示。集成 Chroma 向量库与 BM25 混合检索，具备“动态意图识别”，能根据需求自动增强检索上下文。
*   **基础层 (`langchain_app/`)**：基础演示。虽然是基础模块，但也适配了异步 IO 与统一工具库。

## 🛠️ 技术选型原理

1.  **Hugging Face 本地模型**：在 `rag_app` 中，使用 `sentence-transformers` 家族模型。系统会自动处理从 HF 的加载与缓存，实现 **100% 本地化语义计算**。
2.  **异步优先**：全项目基于 `asyncio` 构建，支持流式输出与高并发交互。
3.  **内存化存储**：为解决 macOS 的文件系统锁问题，SQLite 数据库默认采用 `:memory:` 模式，保证运行丝滑。

## 🚀 快速启动

> [!IMPORTANT]
> **运行环境要求**：必须使用 `./env/venv/bin/python3` 执行脚本，以确保依赖完整。

```bash
# 1. 运行带审批的智能体 (推荐测试)
./env/venv/bin/python3 -m langgraph_app.main

# 2. 运行交互式 RAG (混合检索演示)
./env/venv/bin/python3 rag_app/main.py

# 3. 启动 MCP 服务总线
./env/venv/bin/python3 -m tools.mcp_server
```

## 📄 深度学习路径
想要深入了解底层原理？请查阅 [AI 知识全景路线图](./doc/AI_Knowledge_Roadmap.md)。
