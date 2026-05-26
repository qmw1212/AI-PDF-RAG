# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG-based PDF Q&A system using Streamlit, ChromaDB, and Google Gemini API. Users upload PDFs, the system chunks and indexes the text, then answers questions using retrieved context.

## Environment Setup

### Virtual Environment
Always work within the virtual environment:
```bash
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Dependencies
Install with Chinese mirror for faster downloads:
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

Key dependency: `langchain-text-splitters` (not `langchain.text_splitter`) for text chunking.

### Environment Variables
Required in `.env`:
```
GOOGLE_API_KEY=your_gemini_api_key
```

Get API key from: https://aistudio.google.com/app/apikey

### HuggingFace Model Downloads
The app sets `HF_ENDPOINT='https://hf-mirror.com'` at startup to use Chinese mirror for downloading sentence-transformers models. This must be set before importing other modules.

## Running the Application

```bash
streamlit run app.py
```

Access at http://localhost:8501

**First run**: Downloads ~90MB embedding model (all-MiniLM-L6-v2). Subsequent runs are fast due to caching.

## Architecture

### Module Structure

**app.py** - Streamlit UI and orchestration
- Sets HuggingFace mirror before imports
- Uses `@st.cache_resource` to cache initialized components
- Manages session state for PDF processing status

**pdf_processor.py** - PDF text extraction and chunking
- Uses PyPDF2 for extraction
- Uses `langchain_text_splitters.RecursiveCharacterTextSplitter`
- Default: 1000 char chunks, 200 char overlap

**vector_store.py** - Vector storage and retrieval
- ChromaDB with in-memory client
- Sentence Transformers for embeddings (all-MiniLM-L6-v2)
- Collection name: "pdf_documents"

**gemini_client.py** - LLM integration
- Uses `google.generativeai` package (deprecated, but functional)
- Model: gemini-pro
- Constructs prompts with retrieved context

### Data Flow

1. User uploads PDF → `pdf_processor.process_pdf()`
2. Extract text → chunk into segments
3. Generate embeddings → store in ChromaDB via `vector_store.add_documents()`
4. User asks question → `vector_store.search()` retrieves top-k chunks
5. Chunks + question → `gemini_client.generate_answer()`
6. Display answer in Streamlit

## Common Issues

### Import Errors
- `ModuleNotFoundError: langchain.text_splitter` → Install `langchain-text-splitters` package
- `ModuleNotFoundError: torchvision` → Warnings only, safe to ignore

### Network Issues
- HuggingFace timeout → Ensure `HF_ENDPOINT` is set to `https://hf-mirror.com` before imports
- Gemini API errors → Verify `GOOGLE_API_KEY` in `.env`

### Slow Startup
- First run downloads embedding model (~90MB)
- Check terminal for download progress
- Model cached locally after first download

## Configuration

### Text Chunking
Adjust in `app.py` line 26:
```python
PDFProcessor(chunk_size=1000, chunk_overlap=200)
```

### Retrieval Count
Default: 3 chunks. User can adjust via UI number input.

### Embedding Model
Change in `vector_store.py`:
```python
self.embedding_model = SentenceTransformer('model-name')
```

## Debugging

### Check Gemini API Connection
```python
import google.generativeai as genai
genai.configure(api_key="your_key")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("test")
print(response.text)
```

### Verify ChromaDB
```python
from vector_store import VectorStore
vs = VectorStore()
vs.add_documents(["test doc"])
results = vs.search("test", n_results=1)
print(results)
```

### Check PDF Processing
```python
from pdf_processor import PDFProcessor
processor = PDFProcessor()
with open("test.pdf", "rb") as f:
    chunks = processor.process_pdf(f)
print(f"Generated {len(chunks)} chunks")
```
