# RAG (Retrieval-Augmented Generation) 现代化应用

本模块展示了如何通过混合检索与动态意图识别，构建一个“懂行”的 AI 助手。

## 🧠 核心原理

1.  **混合检索 (Hybrid Search)**：
    *   **向量检索 (Chroma)**：负责捕捉“语义”相似性。
    *   **关键词检索 (BM25)**：负责捕捉“精确匹配”（如特定术语）。
2.  **本地嵌入 (Local Embeddings)**：
    *   使用 `HuggingFaceEmbeddings` 驱动。
    *   默认模型：`sentence-transformers/all-MiniLM-L6-v2`。
3.  **动态增强 (Active RAG)**：
    *   不同于传统的静态 RAG，本模块会在推理时判断是否需要通过外部工具补充实时信息（如天气）。

## 🛠️ Hugging Face 加载流程
首次运行或清除缓存后，系统会自动从 **Hugging Face 开源社区** 下载所需模型。
*   **存放位置**：通常位于 `~/.cache/huggingface`。
*   **安全性**：仅加载公开权重，无需上传您的任何数据。

## 🚀 运行
```bash
./env/venv/bin/python3 rag_app/main.py
```
