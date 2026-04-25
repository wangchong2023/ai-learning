# AI-Learning: 手把手原理与逻辑流转指引

本手册旨在帮助您理解当您输入一个问题时，系统底层究竟发生了什么。

---

## 🧠 1. RAG 引擎：从问题到知识 (Walkthrough)

路径：`rag_app/main.py` -> `utils/factory.py`

### Step 1: 语义召回 (Recall)
当您输入“RAG 是什么”：
1.  系统调用 `ModernHybridRetriever`。
2.  **向量检索 (Chroma)**：捕捉“语义相似性”。
3.  **关键词检索 (BM25)**：捕捉“术语精确匹配”。
4.  **代码实现**：
    ```python
    v_docs = self.vector_retriever.invoke(query)
    b_docs = self.bm25_retriever.invoke(query)
    ```

### Step 2: 深度重排 (Rerank)
召回的 Top-5 知识点会被送入 `ModernReranker`：
*   它对知识点进行二次打分，剔除噪音，只保留最精准的 Top-2。

### Step 3: 动态增强 (Active RAG)
系统判断是否需要外部信息：
*   如果问题涉及“天气/实时”，则调用 `tools/common_tools.py`。

---

## 🛡️ 2. LangGraph：受控的智能体 (Walkthrough)

路径：`langgraph_app/core/`

### Step 1: 节点思考 (Reasoning)
`agent_reasoning_node` 调用 LLM 生成决策：
*   是直接回答？还是需要调用工具？
*   **代码锚点**：`nodes.py` 中的 `llm_with_tools.ainvoke(messages)`。

### Step 2: 人工审批 (HITL)
如果 Agent 想要执行工具：
1.  流程流转到 `tools` 节点前。
2.  **触发中断**：由于 `builder.py` 中配置了 `interrupt_before=["tools"]`。
3.  **等待授权**：系统在控制台挂起，等待您的 `y/n`。

### Step 3: 状态回溯
执行完工具后，结果被追加到 `AgentState` 的 `messages` 序列中，流程返回 `agent` 节点进行总结。

---

## 🤝 3. Multi-Agent：多智能体接力 (Walkthrough)

路径：`multi_agent_app/core/`

### Step 1: 复杂课题拆解 (Researcher)
当您输入一个宏大主题（如“量子计算”）：
1.  流程进入 `researcher_node`。
2.  **动态提取**：研究员调用 LLM，将大课题拆解为数个“核心事实/研究维度”。
3.  **状态流转**：研究员将事实写入状态机的 `research_notes` 字段，并将 `next_agent` 标记为 `writer`。

### Step 2: 动态路由分发 (Router)
LangGraph 的 `add_conditional_edges` 根据 `state["next_agent"]` 的值，将流程精准移交给对应的下一步节点（此处为 Writer）。

### Step 3: 深度融合创作 (Writer)
1.  流程进入 `writer_node`。
2.  **上下文重组**：作家从状态机中读取 `research_notes`。
3.  **定向输出**：作家基于严谨的笔记事实，重新编排语言风格并输出终稿，随后将节点流转至 `END`。

---

## 🗺️ 4. Planner：计划与执行 (Walkthrough)

路径：`planner_app/core/`

### Step 1: 顶层规划 (Planner)
应对包含多个依存条件的宏大指令（如“计算A和B然后对比”）：
1.  **全局视野**：Planner 抛弃 ReAct 走一步看一步的局限，强制使用 Pydantic 生成一张完整的、结构化的“步骤清单” (JSON)。
2.  **状态保存**：清单被写入 `PlanExecuteState["plan"]`。

### Step 2: 无情执行 (Executor)
1.  **单点聚焦**：从清单中弹出第一项，交给大模型（或执行工具）处理。
2.  **结果沉淀**：执行完毕后，结果与步骤名作为元组被追加到 `past_steps` 历史记录中。

### Step 3: 动态复盘 (Replanner)
1.  **自我纠错**：根据 `past_steps`，判断整个大目标是否已完成。
2.  **路由重定向**：如果任务未完结，重新生成修改后的清单，打回给 Executor；如果已完成，输出 Final Response。

---

## 📡 5. 工具发布：MCP 协议 (Walkthrough)

路径：`tools/mcp_server.py`

1.  **自动发现**：`mcp_server.py` 扫描 `mcp_tool_funcs` 字典。
2.  **协议封装**：通过 `FastMCP` 将 Python 函数转化为符合 Anthropic 标准的 JSON-RPC 接口。
3.  **一键发布**：`make mcp` 启动后，外部客户端即可通过 Stdio 调用您的本地代码。

---

## 🛠️ 如何快速修改？

*   **想增加新工具？** 只需要修改 `tools/common_tools.py` 并注册到字典中。
*   **想更换模型？** 修改 `env/.env` 中的 API Key 和 `utils/config.py` 中的模型名称。
*   **想增加测试？** 在 `tests/` 下添加新的 `unittest` 类并运行 `make test`。
