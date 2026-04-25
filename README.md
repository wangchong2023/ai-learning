# AI-Learning: 现代化 AI 应用架构实验场

本项目是一个基于 **LangChain 0.3+**、**LangGraph** 和 **MCP (Model Context Protocol)** 的全栈 AI 实验场。它展示了如何构建一个高度模块化、具备实时感知能力、且拥有人工干预机制的智能体系统。

## 🏗️ 全局架构概览

*   **能力层 (`tools/`)**：中心化工具库，支持跨框架复用及 MCP 发布。
*   **编排层 (`langgraph_app/`)**：高级智能体，支持 **HITL (人工审批流)**。
*   **增强层 (`rag_app/`)**：**Active RAG** 演示，结合本地知识库与动态工具调用。
*   **基础层 (`langchain_app/`)**：初学者 Legacy 演示。

## 🛠️ 技术选型原理

1.  **Hugging Face 本地运行**：在 `rag_app` 中，向量模型从 HF 下载并在您的本地 CPU 运行。**数据不出本地，计算完全免费**。
2.  **内存数据库**：为避开 macOS 文件锁冲突，默认采用 **`:memory:`** 存储。
3.  **统一工具总线**：工具只需定义一次，即可同时供应给 LangChain、LangGraph 和 MCP Server。

## 🚀 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行交互式 RAG
python rag_app/main.py

# 3. 运行带审批的智能体
python -m langgraph_app.main
```
