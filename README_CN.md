# AI-PDF-RAG

中文 | [English](README.md)

**基于 RAG + LLM 的智能 PDF 问答系统**

端到端的 RAG（检索增强生成）应用，支持对 PDF 文档进行智能问答。采用现代 AI 技术栈，包括向量检索、语义搜索和大语言模型。

---

## 项目简介

AI-PDF-RAG 是一个端到端的文档智能系统，能够将静态 PDF 文件转化为可交互的知识库。用户上传文档后，可以用自然语言提问，系统会基于文档内容生成准确的答案。

**为什么选择 RAG？** 传统 LLM 受限于训练数据和上下文窗口。RAG 通过在生成前检索相关文档片段来解决这一问题，实现：
- 基于特定文档的准确回答
- 通过上下文约束减少幻觉
- 无需重新训练即可扩展知识库

**系统思路：** 将语义搜索与生成式 AI 结合。文档经过分块、向量化后存入 ChromaDB。用户查询时触发相似度搜索，检索相关上下文，再送入 LLM 生成答案。

---

## 功能特性

📄 **PDF 上传与处理** — 自动提取文本并智能分块  
🔍 **语义检索** — 基于 Sentence Transformers 的向量相似度搜索  
🧠 **LLM 驱动问答** — 支持多 LLM 提供商的上下文感知答案生成  
⚡ **高效向量搜索** — ChromaDB 实现快速相似度匹配  
🎨 **现代化界面** — 简洁的 Streamlit 界面，实时反馈  
🔧 **模块化架构** — 解耦组件设计，易于扩展  
🌐 **多提供商支持** — 灵活的 LLM 后端（NVIDIA、DeepSeek、Gemini）

---

## 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| **框架** | Python 3.14 | 核心语言 |
| **界面** | Streamlit | Web 界面 |
| **PDF 解析** | PyPDF2 | 文本提取 |
| **文本分割** | LangChain | 语义分块 |
| **向量数据库** | ChromaDB | Embedding 存储与检索 |
| **Embedding 模型** | Sentence Transformers (all-MiniLM-L6-v2) | 文本向量化 |
| **LLM** | NVIDIA / DeepSeek / Gemini | 答案生成 |
| **架构模式** | RAG (Retrieval-Augmented Generation) | 核心架构 |

---

## 系统流程

```
PDF 上传 → 文本提取 → 分块 → 向量化 → ChromaDB → 查询 → 检索 → LLM → 答案
```

**流程详解：**

1. **文档摄入**：使用 PyPDF2 解析 PDF 并提取文本
2. **分块处理**：通过 LangChain 的 RecursiveCharacterTextSplitter 将文本切分为重叠片段（1000 字符，200 字符重叠）
3. **向量化**：使用 Sentence Transformers 将每个文本块转换为 384 维向量
4. **索引构建**：向量及元数据存入 ChromaDB，支持快速检索
5. **查询处理**：用户问题使用相同模型进行向量化
6. **相关检索**：通过余弦相似度检索 Top-K 最相关文本块
7. **答案生成**：将检索到的上下文和问题一起送入 LLM 进行答案合成
8. **结果展示**：显示生成的答案，并提供源文本块以保证透明度

---

## 项目结构

```
AI-PDF/
├── app.py                 # Streamlit 主应用与 UI 编排
├── gemini_client.py       # LLM 客户端（NVIDIA/DeepSeek/Gemini API 封装）
├── pdf_processor.py       # PDF 文本提取与分块逻辑
├── vector_store.py        # ChromaDB 接口，负责 Embedding 存储与检索
├── requirements.txt       # Python 依赖
├── .env.example           # 环境变量模板
├── CLAUDE.md              # AI 助手项目文档
└── README.md              # 英文文档
```

**模块职责：**

- `app.py`：入口文件，处理文件上传、会话状态和 UI 渲染
- `gemini_client.py`：抽象 LLM API 调用，支持多提供商和错误处理
- `pdf_processor.py`：封装 PDF 解析和文本分块，支持参数配置
- `vector_store.py`：管理 ChromaDB 操作（添加、搜索、重置）和 Embedding 生成

---

## 快速开始

### 前置要求

- Python 3.10+
- 以下任一 API 密钥：[NVIDIA](https://build.nvidia.com/)、[DeepSeek](https://platform.deepseek.com/) 或 [Google AI Studio](https://aistudio.google.com/)

### 安装

**Linux / macOS：**

```bash
# 克隆仓库
git clone https://github.com/qmw1212/AI-PDF-RAG.git
cd AI-PDF-RAG

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**Windows：**

```bash
# 克隆仓库
git clone https://github.com/qmw1212/AI-PDF-RAG.git
cd AI-PDF-RAG

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

### 配置

```bash
# 复制环境变量模板
cp .env.example .env  # Linux/macOS
copy .env.example .env  # Windows

# 编辑 .env 文件，添加 API 密钥
# NVIDIA（推荐）：
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx

# DeepSeek：
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx

# Gemini：
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxx
```

### 运行

```bash
streamlit run app.py
```

在浏览器中访问 `http://localhost:8501`。

### 使用方法

1. **上传 PDF**：在侧边栏点击"选择PDF文件"并选择文档
2. **处理文档**：点击"处理PDF"按钮提取并索引内容
3. **提出问题**：在主界面输入框中输入问题
4. **调整检索**：使用"检索块数"滑块控制上下文大小（1-10 块）
5. **获取答案**：点击"🔍 提问"按钮获取 AI 生成的回答
6. **查看来源**：展开"查看检索到的相关内容"查看检索到的文本块

---

## 项目截图

> **说明**：截图即将添加。界面包含侧边栏（PDF 上传）、主区域（问题输入）和可展开区域（查看检索到的文档片段）。

---

## 项目亮点

### 为什么这个项目值得关注

✅ **RAG 实践** — 展示检索增强生成在现代 AI 系统中的实际应用

✅ **向量数据库集成** — ChromaDB 语义搜索和 Embedding 管理的实战经验

✅ **LLM 工程化** — 多提供商 API 集成，包含错误处理、超时管理和降级策略

✅ **生产级模式** — 模块化架构、基于环境的配置和会话状态管理

✅ **AI 应用开发** — 从数据摄入到用户界面的端到端流程

### 适用场景

- **AI/ML 作品集项目** — 展示 RAG、Embedding 和 LLM 集成技能
- **求职应用** — 展示超越模型训练的实际 AI 工程能力
- **学习 RAG** — 清晰、有文档的代码库，便于理解 RAG 架构
- **快速原型开发** — 模块化设计支持轻松替换组件（LLM、Embedding、Vector DB）

### 技术深度

- **语义搜索**：基于稠密 Embedding 的余弦相似度检索实现
- **分块策略**：递归文本分割，带重叠以保留上下文边界
- **多提供商 LLM**：支持 NVIDIA、DeepSeek 和 Gemini API 的抽象层
- **容错机制**：超时处理、API 降级和用户友好的错误提示
- **缓存优化**：Streamlit 资源缓存用于模型初始化，降低延迟

---

## Roadmap

- [ ] 支持多种文件格式（DOCX、TXT、Markdown）
- [ ] 对话历史和多轮对话
- [ ] 高级检索策略（混合搜索、重排序）
- [ ] 部署指南（Docker、云平台）
- [ ] 评估指标（答案质量、检索准确率）
- [ ] 用户认证和文档管理

---

## 贡献

欢迎贡献！请随时提交 Pull Request。对于重大更改，请先开 Issue 讨论您想要改变的内容。

---

## 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件。

---

## 致谢

- [LangChain](https://github.com/langchain-ai/langchain) 提供文本分割工具
- [ChromaDB](https://github.com/chroma-core/chroma) 提供向量数据库
- [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) 提供 Embedding 模型
- [Streamlit](https://github.com/streamlit/streamlit) 提供快速 UI 开发框架

---

## 联系方式

如有问题或反馈，请在 GitHub 上提交 Issue。
