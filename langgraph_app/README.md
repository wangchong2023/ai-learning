# LangGraph 智能体 (HITL 审批流)

本模块是本项目的“大脑”，展示了如何构建具备生产级确定性与安全性的智能体。

## 🛡️ 人工审批 (Human-in-the-loop)
*   **断点机制**：在 `builder.py` 中通过 `interrupt_before=["tools"]` 实现。
*   **安全可控**：Agent 在执行如 `run_python_code` 等高危动作前，会强制暂停。
*   **决策透明**：用户可实时查看模型生成的工具调用参数，并决定是否继续。

## 🏗️ 状态机架构
*   `core/state.py`：定义状态结构。
*   `core/nodes.py`：核心推理节点，通过 **`utils.factory`** 接入统一配置的 LLM。
*   `core/builder.py`：将节点连接为有向图，并注入 `MemorySaver` 持久化层。

## 🚀 运行
```bash
./env/venv/bin/python3 -m langgraph_app.main
```
