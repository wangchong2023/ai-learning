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

---

## 🚀 大模型微调 (Fine-Tuning) 通用工作流总结

无论是使用 Qwen 还是 Llama，现代大模型微调（特别是基于 **Unsloth** 或 **PEFT** 的高效微调）通常遵循以下标准化流程。您可以参考本目录下的代码进行复现：

### 1. 环境与模型加载
*   **依赖安装**：通常需要安装 `transformers`, `trl`, `peft`, `accelerate` 以及加速库（如 `unsloth` 或 `flash-attn`）。
*   **模型量化加载**：为了能在单张消费级显卡（如 RTX 4090 或 T4）上微调 7B~35B 的模型，通常在加载时开启 **4-bit 量化 (BitsAndBytes)**。

### 2. 注入 LoRA 适配器
*   全量参数微调成本极高，因此我们通常使用 **LoRA (Low-Rank Adaptation)**。
*   **配置参数**：向模型的关键层（如 `q_proj`, `k_proj`, `v_proj`, `o_proj`）注入低秩矩阵。通常设置 `r=16` 或 `r=32`，`lora_alpha=32`。这意味着您只需要训练大约 1% 的模型参数。

### 3. 数据集格式化
*   大模型对训练数据的格式要求极其严格。需要将您的业务数据转换为标准的 **ChatML** 或 **Alpaca** 对话格式。
*   通过 `tokenizer.apply_chat_template` 映射并对文本进行 Tokenize。

### 4. 训练与强化学习 (RLHF/GRPO)
*   **SFT (监督微调)**：使用 `SFTTrainer` 传入数据集进行 Next-Token 预测训练。设置 `learning_rate`（通常为 2e-4）、`batch_size` 和优化器（如 `adamw_8bit`）。
*   **GRPO (强化学习)**：如果您参考了 `Llama-3.2-3B-R1-Zero-GRPO.ipynb`，它展示了更高级的对齐方法：通过自定义奖励函数（如“格式是否符合XML”、“答案是否正确”）让模型在不断试错中提升逻辑推理能力。

### 5. 推理测试与合并导出
*   训练完成后，使用 `FastLanguageModel.for_inference()` 开启 2 倍速推理进行效果验证。
*   验证满意后，将 LoRA 权重与基础模型合并（Merge to 16bit / GGUF格式），并使用 `push_to_hub` 上传至 Hugging Face 或下载到本地用于生产部署。
