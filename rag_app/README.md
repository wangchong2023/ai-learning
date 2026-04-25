# RAG (Retrieval-Augmented Generation) 现代化应用

本模块展示了如何通过两阶段检索与动态意图识别，构建一个生产级的 AI 助手。

## 🧠 核心原理

1.  **两阶段检索架构 (Recall -> Rerank)**：
    *   **召回 (Recall)**：利用 **Chroma (向量)** 和 **BM25 (关键词)** 进行混合粗筛。
    *   **重排 (Rerank)**：通过 `ModernReranker` 模块对候选文档进行二次语义对齐，选出最优上下文。
2.  **本地嵌入 (Local Embeddings)**：
    *   通过 **`utils.factory`** 统一初始化 `HuggingFaceEmbeddings`。
3.  **动态增强 (Active RAG)**：
    *   在推理时根据意图自动决定是否调用外部工具来补充实时信息。

## 🛠️ 模型加载说明
系统会自动从 **Hugging Face** 下载模型并缓存至本地。
*   **缓存管理**：可在 `utils/config.py` 中自定义模型存放路径。

## 🚀 运行
```bash
# 推荐使用根目录 Makefile 命令
make rag

# 或者直接运行
./env/venv/bin/python3 rag_app/main.py
```
