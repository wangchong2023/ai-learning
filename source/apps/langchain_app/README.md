# LangChain 基础演示

本模块展示了如何使用 LangChain 0.3+ 构建标准的智能体调用链路。

## 🌟 核心特性
*   **异步支持**：采用 `ainvoke` 与 `astream` 实现高效交互。
*   **工具绑定**：直接引用项目根目录 `tools/common_tools.py` 中的统一工具。
*   **内存化持久化**：使用 `AsyncSqliteSaver` 管理会话记忆，默认存放在内存中。

## 🚀 运行
```bash
./env/venv/bin/python3 langchain_app/main.py
```
