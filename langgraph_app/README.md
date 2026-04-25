# LangGraph 智能体 (HITL 审批流)

本模块展示了如何使用 LangGraph 构建具备人机交互能力的复杂状态机。

## 🛡️ 人工审批 (Human-in-the-loop)
*   **安全保障**：所有工具执行前均会触发中断。
*   **控制权**：用户可以查看 Agent 申请执行的工具及其参数，并决定授权 (`y`) 或拒绝 (`n`)。

## 🏗️ 模块化设计
*   `core/state.py`：定义状态结构。
*   `core/nodes.py`：定义推理与执行节点。
*   `core/builder.py`：编排逻辑与中断策略。

## 🚀 运行
```bash
python -m langgraph_app.main
```
