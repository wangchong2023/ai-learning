# Tools: 统一能力总线

本项目的所有工具均集中在此处定义，遵循“定义一次，多处运行”的原则。

## 🧩 核心工具说明

1.  **`run_python_code`**：执行 Python 代码分析。
2.  **`fetch_real_weather`**：获取指定城市的实时环境数据。
3.  **`calculate`**：执行高精度数学运算。

## 📡 分发与监控机制

*   **内部调用**：直接通过 `from tools.common_tools import tools` 引用。
*   **全链路日志**：所有工具执行细节均由 **`utils.logger`** 实时记录，方便审计。
*   **MCP 发布**：
    ```bash
    ./env/venv/bin/python3 -m tools.mcp_server
    ```
    发布后，任何支持 MCP 的客户端均可接入。

## ⚠️ 开发注意事项
*   工具函数必须包含详尽的 `docstring`，这是 LLM 识别其用途的唯一依据。
*   工具名称需全局唯一，避免 `400 BadRequest` 错误。
