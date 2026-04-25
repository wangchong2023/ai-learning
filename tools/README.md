# Tools: 统一能力总线

本项目的所有工具均集中在此处定义，遵循“定义一次，多处运行”的原则。

## 🧩 核心工具说明

1.  **`run_python_code`**：
    *   **逻辑**：在本地 Python 环境中动态执行代码。
    *   **用途**：处理复杂的数学运算或逻辑推演。
2.  **`fetch_real_weather`**：
    *   **逻辑**：通过网络请求获取实时天气。
    *   **用途**：演示智能体如何获取实时外部信息。
3.  **`calculate`**：
    *   **逻辑**：基础算术运算。
    *   **用途**：原子工具调用演示。

## 📡 分发机制

*   **LangChain/LangGraph**：直接通过 `from tools.common_tools import tools` 引用。
*   **MCP 发布**：
    ```bash
    ./env/venv/bin/python3 -m tools.mcp_server
    ```
    发布后，任何支持 MCP 的客户端（如 Claude Desktop）均可接入。

## ⚠️ 开发注意事项
*   工具函数必须包含详尽的 `docstring`，这是 LLM 识别其用途的唯一依据。
*   工具名称需全局唯一，避免 `400 BadRequest` 错误。
