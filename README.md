# AI-PDF-RAG

[中文文档](README_CN.md) | English

**Intelligent PDF Question Answering System powered by RAG + LLM**

An end-to-end RAG (Retrieval-Augmented Generation) application that enables intelligent question answering over PDF documents. Built with modern AI stack including vector search, semantic retrieval, and large language models.

---

## Overview

AI-PDF-RAG is an end-to-end document intelligence system that transforms static PDF files into interactive knowledge bases. Users can upload documents, ask questions in natural language, and receive accurate answers grounded in the document content.

**Why RAG?** Traditional LLMs are limited by their training data and context windows. RAG addresses this by retrieving relevant document chunks before generation, enabling:
- Accurate answers grounded in specific documents
- Reduced hallucination through context grounding
- Scalable knowledge base without retraining models

**System Approach:** The pipeline combines semantic search with generative AI. Documents are chunked, embedded into vector space, and stored in ChromaDB. User queries trigger similarity search to retrieve relevant context, which is then fed to an LLM for answer generation.

---

## Features

📄 **PDF Upload & Processing** — Automatic text extraction and intelligent chunking  
🔍 **Semantic Retrieval** — Vector similarity search powered by Sentence Transformers  
🧠 **LLM-Powered QA** — Context-aware answer generation with multi-provider support  
⚡ **Fast Vector Search** — ChromaDB for efficient similarity matching  
🎨 **Modern UI** — Clean Streamlit interface with real-time feedback  
🔧 **Modular Architecture** — Decoupled components for easy extension  
🌐 **Multi-Provider Support** — Flexible LLM backend (NVIDIA, DeepSeek, Gemini)

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Python 3.14 | Core language |
| **UI** | Streamlit | Web interface |
| **PDF Parser** | PyPDF2 | Text extraction |
| **Text Splitter** | LangChain | Semantic chunking |
| **Vector DB** | ChromaDB | Embedding storage & retrieval |
| **Embedding Model** | Sentence Transformers (all-MiniLM-L6-v2) | Text vectorization |
| **LLM** | NVIDIA / DeepSeek / Gemini | Answer generation |
| **Architecture** | RAG (Retrieval-Augmented Generation) | Core pattern |

---

## System Workflow

```
PDF Upload → Text Extraction → Chunking → Embedding → ChromaDB → Query → Retrieval → LLM → Answer
```

**Pipeline Breakdown:**

1. **Document Ingestion**: PDF files are parsed and text is extracted using PyPDF2
2. **Chunking**: Text is split into overlapping segments (1000 chars, 200 overlap) via LangChain's RecursiveCharacterTextSplitter
3. **Embedding**: Each chunk is converted to a 384-dim vector using Sentence Transformers
4. **Indexing**: Vectors are stored in ChromaDB with metadata for fast retrieval
5. **Query Processing**: User questions are embedded using the same model
6. **Retrieval**: Top-k most similar chunks are retrieved via cosine similarity
7. **Generation**: Retrieved context + question are sent to LLM for answer synthesis
8. **Response**: Generated answer is displayed with source chunks for transparency

---

## Project Structure

```
AI-PDF/
├── app.py                 # Streamlit main application & UI orchestration
├── gemini_client.py       # LLM client (NVIDIA/DeepSeek/Gemini API wrapper)
├── pdf_processor.py       # PDF text extraction & chunking logic
├── vector_store.py        # ChromaDB interface for embedding storage/retrieval
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── CLAUDE.md              # Project documentation for AI assistants
└── README.md              # This file
```

**Module Responsibilities:**

- `app.py`: Entry point, handles file uploads, session state, and UI rendering
- `gemini_client.py`: Abstracts LLM API calls with multi-provider support and error handling
- `pdf_processor.py`: Encapsulates PDF parsing and text chunking with configurable parameters
- `vector_store.py`: Manages ChromaDB operations (add, search, reset) and embedding generation

---

## Quick Start

### Prerequisites

- Python 3.10+
- API key from one of: [NVIDIA](https://build.nvidia.com/), [DeepSeek](https://platform.deepseek.com/), or [Google AI Studio](https://aistudio.google.com/)

### Installation

**Linux / macOS:**

```bash
# Clone the repository
git clone https://github.com/qmw1212/AI-PDF-RAG.git
cd AI-PDF-RAG

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows:**

```bash
# Clone the repository
git clone https://github.com/qmw1212/AI-PDF-RAG.git
cd AI-PDF-RAG

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env  # Linux/macOS
copy .env.example .env  # Windows

# Edit .env and add your API key
# For NVIDIA (recommended):
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx

# For DeepSeek:
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx

# For Gemini:
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxx
```

### Run

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

### Usage

1. **Upload PDF**: Click "选择PDF文件" in the sidebar and select a document
2. **Process**: Click "处理PDF" to extract and index the content
3. **Ask Questions**: Enter your question in the main interface
4. **Adjust Retrieval**: Use the "检索块数" slider to control context size (1-10 chunks)
5. **Get Answers**: Click "🔍 提问" to receive AI-generated responses
6. **View Sources**: Expand "查看检索到的相关内容" to see retrieved chunks

---

## Screenshots

> **Note**: Screenshots will be added soon. The interface includes a sidebar for PDF upload, main area for question input, and expandable sections for viewing retrieved document chunks.

---

## Project Highlights

### Why This Project Matters

✅ **RAG Implementation** — Demonstrates practical application of Retrieval-Augmented Generation, a core pattern in modern AI systems

✅ **Vector Database Integration** — Hands-on experience with ChromaDB for semantic search and embedding management

✅ **LLM Engineering** — Multi-provider API integration with error handling, timeout management, and fallback strategies

✅ **Production Patterns** — Modular architecture, environment-based configuration, and session state management

✅ **AI Application Development** — End-to-end pipeline from data ingestion to user-facing interface

### Ideal For

- **AI/ML Portfolio Projects** — Showcases RAG, embeddings, and LLM integration skills
- **Job Applications** — Demonstrates practical AI engineering beyond model training
- **Learning RAG** — Clean, documented codebase for understanding RAG architecture
- **Rapid Prototyping** — Modular design allows easy swapping of components (LLM, embeddings, vector DB)

### Technical Depth

- **Semantic Search**: Implements cosine similarity-based retrieval over dense embeddings
- **Chunking Strategy**: Recursive text splitting with overlap to preserve context boundaries
- **Multi-Provider LLM**: Abstraction layer supporting NVIDIA, DeepSeek, and Gemini APIs
- **Error Resilience**: Timeout handling, API fallback, and user-friendly error messages
- **Caching**: Streamlit resource caching for model initialization to reduce latency

---

## Roadmap

- [ ] Support for multiple file formats (DOCX, TXT, Markdown)
- [ ] Conversation history and multi-turn dialogue
- [ ] Advanced retrieval strategies (hybrid search, reranking)
- [ ] Deployment guide (Docker, cloud platforms)
- [ ] Evaluation metrics (answer quality, retrieval accuracy)
- [ ] User authentication and document management

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for text splitting utilities
- [ChromaDB](https://github.com/chroma-core/chroma) for vector database
- [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) for embedding models
- [Streamlit](https://github.com/streamlit/streamlit) for rapid UI development

---

## Contact

For questions or feedback, please open an issue on GitHub.
