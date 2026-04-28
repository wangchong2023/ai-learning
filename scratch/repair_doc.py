import re
import os

path = '/Users/constantine/Documents/work/code/projects/ai-learning/doc/AI_Knowledge_Roadmap.md'
if not os.path.exists(path):
    print(f"Error: {path} not found")
    exit(1)

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Define the CLEAN RAG Block
clean_rag = r'''#### 6.6.4. 检索增强生成 (RAG)
**本质解析**：它是 **“给大脑配上的实时图书馆”**。模型不再依赖过时的记忆，而是通过检索外部最新资料来回答问题，彻底解决时效性与幻觉问题。

**核心技术链路 (RAG 全生命周期)**

RAG 系统由两个核心闭环组成：**离线知识摄入 (Indexing)** 与 **在线检索生成 (Querying)**。

```mermaid
graph TD
    %% 离线摄入
    subgraph Ingestion ["1. 离线摄入 (Data Ingestion)"]
        D["原始文档 (PDF/MD)"] --> P["解析与清洗 (Parser)"]
        P --> S["语义切块 (Chunking)"]
        S --> E["向量化 (Embedding)"]
        E --> DB[("向量数据库 ([Vector DB](#212-向量数据库选型与优化))")]
    end

    %% 在线检索
    subgraph QueryFlow ["2. 在线检索 (Retrieval Flow)"]
        UserQuery["用户提问 (Query)"] --> Rewrite["查询改写 (Rewrite)"]
        Rewrite --> Dense["向量召回"]
        Rewrite --> Keyword["关键词召回"]
        Dense & Keyword --> RRF["RRF 融合 (秩融合)"]
        Rerank["重排 (Re-rank)"]
    end

    DB -.-> Dense
    DB -.-> Keyword

    %% 生成阶段
    Rerank -- "精选 Top-K" --> LLM["3. LLM 增强生成"]
    LLM --> Final["最终答案 (Final Result)"]

    style Ingestion fill:#f8fafc,stroke:#334155,stroke-dasharray: 5 5
    style QueryFlow fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

**核心环节深度解析**：

1. **离线摄入 (Indexing)**：
    - **分块切分 (Chunking)**：将原始文档拆解为模型可消化的“碎片”。建议保持 **10-20% 的重叠度 (Overlap)**，防止上下文断层。
    - **向量化 (Embedding)**：利用嵌入模型将文字转化为高维坐标，实现“语义距离”的数学表达。
2. **查询改写 (Query Rewrite)**：利用 LLM 将模糊提问转化为检索亲和力更强的描述（如补全缩写、Hypothetical Document Embeddings/HyDE），从而**扩大召回范围**。
3. **混合召回与 RRF (Hybrid & RRF)**：
    - **语义召回**：基于 **余弦相似度 (Cosine Similarity)** 进行匹配。
    - **BM25**：处理专业术语、产品型号等必须精准匹配的情况。
    - **RRF (Reciprocal Rank Fusion)**：通过算法将向量和关键词两路不同的得分体系“大一统”，形成最终的检索排序清单。
4. **召回评估与重排 (Evaluation & Re-rank)**：
    - **Recall@K**：衡量检索链路末端是否精准捕获了目标答案。
    - **Re-rank**：引入 Cross-Encoder 模型对召回的碎片进行深度二次打分，剥离噪音。
5. **增强生成**：将重排后的事实与提问拼接，强制模型“按图索骥”生成回答。

**第三层：工程优化哲学 (提高信噪比)**

> [!IMPORTANT]
> 💡 **RAG 工程化金律 (The 3C Rule)**:
> 1. **Chunking (切分)**：宁可重叠，不可断句。
> 2. **Context (上下文)**：宁可精炼，不可堆砌。
> 3. **Consolidation (整合)**：宁可重排，不可直推。
'''

# 2. Define the CLEAN Transition
clean_13_14 = r'''### 13.3. 模型 API 聚合与路由
在工业实践中，为了降低对接成本并实现故障自动切换（Failover），通常使用聚合服务或路由中台。

| 聚合工具/服务 | 类型 | 核心能力 | 代表模型/特性 | 官网/链接 |
| :--- | :--- | :--- | :--- | :--- |
| **OpenRouter** | **云端服务** | 全球最全的模型聚合平台，统一 OpenAI 标准格式接口 | 支持 GPT, Claude, Llama, DeepSeek 等 100+ 模型 | [OpenRouter](https://openrouter.ai/) |
| **SiliconFlow (硅基流动)** | **云端服务** | 国内领先的高性能推理平台，极致的 DeepSeek 部署速度 | 极速版 DeepSeek-V3/R1，支持主流国产开源模型 | [SiliconFlow](https://siliconflow.cn/) |
| **LiteLLM** | **开源框架** | 本地代理网关，将各厂商非标 API 转化为 OpenAI 格式 | 支持负载均衡、Token 统计与企业级 API 治理 | [LiteLLM](https://github.com/BerriAI/litellm) |

---

# 🌟 第三篇：工具与框架
> 本篇聚焦于构建具备逻辑闭环、安全护栏与自我进化能力的**企业级智能体**。我们将探讨如何将原子工具组装为生产力引擎，重点涵盖 **Agentic RAG**、**智能体治理**以及垂直领域推理训练实战。

---

## 14. 质量评估与可观测性
> **工程思想：评估驱动开发 (Evaluation-Driven Development, EDD)**
传统的单元测试无法衡量 AI 输出的质量。在编写首行代码前，架构师必须定义 **黄金测试集 (Golden Dataset)**，并引入 RAGAS 等框架进行客观打分。

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

# 1. 准备黄金测试数据集
data_samples = {
    'question': ['如何重置密码？'],
    'answer': ['您可以点击登录页面的"忘记密码"进行重置。'],
    'contexts': [['用户可以通过点击忘记密码链接并按照邮件说明重置。']],
    'ground_truth': ['点击忘记密码链接并通过邮件重置。']
}
dataset = Dataset.from_dict(data_samples)

# 2. 执行多维度量化评分
score = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy]
)

# 3. 输出评估报表
print(score.to_pandas()) 
```
'''

# 3. Apply replacements
# Fix RAG (use non-indexed pattern to be safe)
content = re.sub(r'#### \d+\.\d+\.\d+\. 检索增强生成.*?### \d+\.\d+\. 智能体工程', clean_rag + '\n\n### 6.7. 智能体工程', content, flags=re.DOTALL)

# Fix Section 13/14 transition
content = re.sub(r'### \d+\.\d+\. 模型 API 聚合与路由.*?## 14\. 治理、安全与审计工具', clean_13_14 + '\n\n## 14. 治理、安全与审计工具', content, flags=re.DOTALL)

# Final cleanup of empty headers
content = re.sub(r'### \d+\.\d+\.\s+\n', '', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Repair completed successfully.")
