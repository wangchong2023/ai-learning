# 📓 AI-Learning 实验与微调笔记 (Notebooks)

此目录包含了项目相关的**离线实验环境**、**大模型微调 (Fine-tuning)** 以及**强化学习**相关的 Jupyter Notebooks 脚本。这些代码主要用于研究、训练和跑分，不参与在线应用（`source/apps/`）的业务逻辑。

## 📁 内容概览

| 文件名 | 平台环境 | 描述说明 |
| :--- | :--- | :--- |
| `Llama-3.2-3B-R1-Zero-GRPO.ipynb` | 离线实验 | 使用 GRPO 算法对 Llama 3.2 (3B) 进行强化学习（RLHF/R1）实验与训练的完整脚本。 |
| `Qwen3.5-9B-Neo-Kaggle.ipynb` | Kaggle | 在 Kaggle 平台上微调或推理 Qwen3.5 (9B) 模型的执行代码。 |
| `Qwopus-3.5-35B-A3B-Kaggle.ipynb`| Kaggle | 针对 35B 级别大语言模型的进阶实验与训练记录。 |
| `Qwopus3-5-27b-Colab.ipynb` | Google Colab | 在 Colab T4/A100 环境下加载并测试 27B 参数大模型的实验环境。 |

## 🌟 特点
*   **全中文支持**：为降低阅读门槛，所有 Notebook 文件内的 Markdown 说明单元格均已由 AI 进行深度中文翻译，且保留了原始的数学公式与逻辑高亮。
*   **即插即用**：建议直接将对应的文件上传至 Kaggle 或 Google Colab，即可一键利用云端 GPU 资源进行复现。

## ⚠️ 注意事项
*   此处环境独立：若要在本地运行这些 Notebook，请注意它们可能需要 PyTorch, Unsloth, vLLM 等重型依赖，这与根目录的基础 `requirements.txt` 不同，建议根据每个 Notebook 第一个代码块的 `!pip install` 自行配置虚拟环境。
