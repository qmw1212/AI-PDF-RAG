# PDF问答系统

基于RAG（检索增强生成）的PDF文档问答系统，使用Gemini API生成答案。

## 功能特性

- 📤 上传PDF文档
- 📝 自动提取文本内容
- ✂️ 智能文本分块
- 🔍 向量化索引和检索
- 💬 基于Gemini的智能问答
- 🎨 友好的Streamlit界面

## 安装步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置API密钥：
```bash
cp .env.example .env
```
然后编辑`.env`文件，填入你的Gemini API密钥。

3. 运行应用：
```bash
streamlit run app.py
```

## 使用方法

1. 在侧边栏上传PDF文件
2. 点击"处理PDF"按钮
3. 在主界面输入问题
4. 点击"提问"获取答案

## 项目结构

```
AI-PDF/
├── app.py              # Streamlit主应用
├── pdf_processor.py    # PDF处理模块
├── vector_store.py     # 向量存储模块
├── gemini_client.py    # Gemini API客户端
├── requirements.txt    # 依赖列表
├── .env.example        # 环境变量模板
└── README.md          # 项目说明
```

## 技术栈

- **前端框架**: Streamlit
- **PDF处理**: PyPDF2
- **文本分割**: LangChain
- **向量数据库**: ChromaDB
- **嵌入模型**: Sentence Transformers
- **LLM**: Google Gemini Pro
