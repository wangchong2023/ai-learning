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

## 📡 3. 工具发布：MCP 协议 (Walkthrough)

路径：`tools/mcp_server.py`

1.  **自动发现**：`mcp_server.py` 扫描 `mcp_tool_funcs` 字典。
2.  **协议封装**：通过 `FastMCP` 将 Python 函数转化为符合 Anthropic 标准的 JSON-RPC 接口。
3.  **一键发布**：`make mcp` 启动后，外部客户端即可通过 Stdio 调用您的本地代码。

---

## 🛠️ 如何快速修改？

*   **想增加新工具？** 只需要修改 `tools/common_tools.py` 并注册到字典中。
*   **想更换模型？** 修改 `env/.env` 中的 API Key 和 `utils/config.py` 中的模型名称。
*   **想增加测试？** 在 `tests/` 下添加新的 `unittest` 类并运行 `make test`。
