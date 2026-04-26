# AI-Learning: 现代化 AI 应用架构实验场

本项目是一个基于 **LangChain 0.3+**、**LangGraph** 和 **MCP (Model Context Protocol)** 的全栈 AI 实验场。它展示了如何构建一个高度模块化、具备实时感知能力、且拥有人工干预机制的智能体系统。

## 🏗️ 全局架构概览

*   **能力层 (`source/tools/`)**：中心化工具库。采用“定义一次，多处运行”的原则。
*   **规划层 (`source/planner_app/`)**：高级复杂规划。实现 **Plan-and-Execute** 模式，分离逻辑拆解与具体执行。
*   **协作层 (`source/multi_agent_app/`)**：多智能体协作。展示研究员与作家如何分工接力。
*   **编排层 (`source/langgraph_app/`)**：核心高级智能体。基于图的状态机架构，集成 **HITL (人工审批流)**。
*   **增强层 (`source/rag_app/`)**：**Active RAG** 演示。集成两阶段检索 (Recall -> Rerank) 架构。
*   **公共层 (`source/utils/`)**：项目基石。包含配置中心、结构化日志及 **LangSmith 可观测性** 接入。
*   **测试层 (`source/tests/`)**：质量保障。包含自动化集成测试用例。

## 🛠️ 技术选型原理

1.  **两阶段检索架构**：在 `source/rag_app` 中实现召回与精排分离，显著提升回答质量。
2.  **混合存储策略**：
    *   **短时记忆**：默认使用 **`:memory:`** 以规避并发冲突。
    *   **长时知识**：通过配置文件指定磁盘持久化路径。
3.  **组件工厂模式**：通过 `source/utils/factory.py` 统一创建 LLM 与 Embeddings。

## 🚀 运行与维护

本项目引入了 **Makefile** 以简化开发流程，并集成了 **GitHub Actions** 进行自动化质量监控。

```bash
# 1. 运行自动化系统测试 (验证工程地基)
make test

# 2. 运行现代化 RAG 应用 (Recall -> Rerank 架构)
make rag

# 3. 启动多智能体协作实验室
make multi

# 4. 运行高级深度规划实验室 (Plan & Execute)
make plan

# 5. 运行带审批流的智能体 (LangGraph HITL)
make graph

# 6. 启动 MCP 服务总线
make mcp
```

## 🔍 调试与监控 (LangSmith)

本项目深度集成了 **LangSmith**。如需启用：
1. 在 `env/.env` 中设置 `LANGSMITH_TRACING=true`。
2. 填入您的 `LANGSMITH_API_KEY`。
3. 访问 [LangSmith 控制台](https://smith.langchain.com) 查看全链路 Trace。

## 📄 深度指引与原理
*   **[手把手原理与代码指引](./doc/Walkthrough.md)**：详细解析 RAG、LangGraph 与 MCP 的底层流转逻辑。
*   **[AI 知识全景路线图](./doc/AI_Knowledge_Roadmap.md)**：覆盖从硬件到 Agent 治理的全维技术栈。

## 🧠 核心逻辑流转 (Step-by-Step)

1.  **用户输入** -> `source/rag_app` 启动混合检索。
2.  **知识召回** -> `ModernHybridRetriever` (Chroma + BM25) 粗筛。
3.  **精排重排序** -> `ModernReranker` 深度对齐，锁定最强上下文。
4.  **智能体决策** -> `source/langgraph_app` 分析上下文并生成 `tool_calls`。
5.  **人工审批 (HITL)** -> 系统在执行工具前自动挂起，等待 `make graph` 控制台确认。
6.  **最终输出** -> 总结所有知识与工具结果，输出精准答复。
