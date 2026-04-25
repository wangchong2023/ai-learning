# Tools: 统一能力总线

本项目的所有工具均集中在此处定义，实现“定义一次，多处运行”。

## 🧩 核心工具
*   `run_python_code`：代码执行沙箱。
*   `fetch_real_weather`：多城市实时天气抓取。
*   `calculate`：数学运算。

## 📡 发布为 MCP 服务
```bash
python -m tools.mcp_server
```
发布后，任何 MCP 客户端均可接入这些能力。
