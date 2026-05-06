# 🌍 RAG IPCC — Climate Q&A System

A Retrieval-Augmented Generation (RAG) system powered by local LLMs that enables intelligent question-answering over IPCC AR6 climate reports. Built with **Ollama**, **LangChain**, and **Chroma**, this project allows users to ask complex questions about climate change with cited sources from official IPCC documents.

---

## 🎯 Features

- ✅ **Local LLM Processing** — Run everything locally with Ollama (no API keys required)
- 🔍 **Intelligent Retrieval** — Semantic search over PDF documents using vector embeddings
- 📚 **Source Attribution** — Get answers with direct citations to source documents and page numbers
- 🌐 **Web Interface** — User-friendly Streamlit UI for asking questions
- ⚡ **REST API** — FastAPI backend for programmatic access
- 📄 **IPCC AR6 Focus** — Pre-configured for Sixth Assessment Report documents on climate change
- 🔧 **Modular Architecture** — Easily extensible for other document collections

---

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend UI                        │
│              (ui_streamlit.py - localhost:8501)                 │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (app.py)                       │
│              (localhost:8000 - /ask endpoint)                   │
│                                                                 │
│  RAG Chain: Query → Retriever → LLM → Answer + Sources         │
└────────┬────────────────────────────────────┬──────────────────┘
         │                                    │
         ▼                                    ▼
    ┌────────────────────┐        ┌──────────────────────┐
    │  Chroma Vector DB  │        │  Ollama LLM Server   │
    │  (vectordb/)       │        │  • llama3.2:3b       │
    │  • Embeddings      │        │  • nomic-embed-text  │
    │  • Similarity      │        │                      │
    │    Search          │        │  (localhost:11434)   │
    └────────────────────┘        └──────────────────────┘
         ▲
         │ (embeddings.py - initializes)
         │
    ┌────────────────────────────────────┐
    │  PDF Processing & Chunking         │
    │  (ingest.py)                       │
    │  • Load PDFs from data/            │
    │  • Split into 1000-char chunks     │
    │  • Store as JSON in chunks/        │
    └────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Ollama** installed and running (download from [ollama.ai](https://ollama.ai))
- **IPCC AR6 PDFs** in the `data/` folder

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/rag-ipcc.git
cd rag-ipcc

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Ollama Models

```bash
# Terminal 1: Start Ollama server
ollama serve

# Terminal 2: Pull required models
ollama pull llama3.2:3b
ollama pull nomic-embed-text:latest
```

### 3. Prepare Your Data

Place IPCC AR6 PDF files in the `data/` folder:
```
data/
├── IPCC_AR6_SYR_FullVolume.pdf
├── IPCC_AR6_WGI_SPM.pdf
└── IPCC_AR6_SYR_SPM.pdf
```

### 4. Ingest Documents

```bash
# Process PDFs and create chunks
python ingest.py
```

Output:
```
📄 Processing: data/IPCC_AR6_SYR_FullVolume.pdf
✅ Saved 1245 chunks → chunks/IPCC_AR6_SYR_FullVolume.pdf.json
```

### 5. Create Vector Embeddings

```bash
# Generate embeddings and populate vector database
python embeddings.py
```

Output:
```
🔧 Initialisation des embeddings Ollama...
📦 3245 chunks à vectoriser...
✅ Vector DB sauvegardée dans 'vectordb/'
```

### 6. Start the Backend API

```bash
# Terminal 3: Start FastAPI server
uvicorn app:app --reload --port 8000
```

API will be available at `http://localhost:8000`

### 7. Launch the Web UI

```bash
# Terminal 4: Start Streamlit
streamlit run ui_streamlit.py
```

Open browser to `http://localhost:8501` and start asking questions!

---

## 💻 Usage

### Via Web Interface (Recommended)

1. Open the Streamlit app
2. Type your climate-related question
3. Click "Ask 🔍"
4. View the AI-generated answer with cited sources

**Example Questions:**
- "What are the main causes of global warming according to AR6?"
- "What mitigation strategies are recommended for climate change?"
- "How much will sea levels rise by 2100?"

### Via REST API

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the impact of climate change on biodiversity?"}'
```

**Response:**
```json
{
  "answer": "According to the IPCC AR6 reports, climate change poses significant threats to biodiversity through habitat loss, altered precipitation patterns, and temperature shifts...",
  "sources": [
    {
      "source": "data/IPCC_AR6_SYR_FullVolume.pdf",
      "page": "142",
      "preview": "Climate change impacts on biodiversity are widespread and severe..."
    }
  ]
}
```

---

## 📊 Results Example

![RAG Demo Results](data/rag_results.png)

*The system successfully retrieves relevant IPCC documents and generates contextual answers with proper source attribution.*

---

## 📁 Project Structure

```
rag-ipcc/
├── app.py                  # FastAPI backend with RAG chain
├── embeddings.py           # Embedding generation & vector DB init
├── ingest.py              # PDF processing & chunking
├── ui_streamlit.py        # Streamlit web interface
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── data/                  # Raw PDF files (add your PDFs here)
├── chunks/                # Processed PDF chunks (JSON format)
├── vectordb/              # Chroma vector database (auto-created)
└── env/                   # Virtual environment
```

---

## 🔧 Configuration

### LLM Model Selection

Edit `app.py` to change the language model:

```python
llm = ChatOllama(model="llama2:13b", temperature=0.0)  # Use larger model
```

Available Ollama models:
- `llama3.2:3b` (fast, lightweight)
- `llama2:7b` (balanced)
- `llama2:13b` (more capable)
- `neural-chat:7b` (optimized for chat)

### Embedding Model

Edit `embeddings.py` and `app.py`:

```python
embedding_fn = OllamaEmbeddings(model="nomic-embed-text:latest")
```

### Retrieval Parameters

Adjust in `app.py`:

```python
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}  # Number of chunks to retrieve
)
```

### Chunk Size

Edit `ingest.py`:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Characters per chunk
    chunk_overlap=200       # Overlap between chunks
)
```

---

## 🛠️ Troubleshooting

### Issue: "Backend not started" error in Streamlit

**Solution:**
```bash
# Ensure FastAPI is running in another terminal
uvicorn app:app --reload --port 8000
```

### Issue: Ollama models not found

**Solution:**
```bash
# Verify Ollama is running and pull models
ollama list
ollama pull llama3.2:3b
ollama pull nomic-embed-text:latest
```

### Issue: Slow response times

**Solution:**
- Use a faster model: `llama3.2:3b` instead of larger models
- Reduce chunk retrieval: Lower `k` value from 4 to 2
- Increase `chunk_overlap` in `ingest.py` for better context

### Issue: Memory issues

**Solution:**
- Use quantized models (e.g., `llama2:7b` instead of 13b)
- Reduce `chunk_size` in `ingest.py`
- Process PDFs in batches

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | LLM orchestration framework |
| `langchain-ollama` | Ollama integration |
| `langchain-community` | Vector store utilities |
| `chromadb` | Vector database |
| `fastapi` | Web API framework |
| `streamlit` | Web UI framework |
| `PyPDF2` / `pypdf` | PDF processing |
| `unstructured[pdf]` | Advanced document parsing |

See `requirements.txt` for exact versions.

---

## 🚀 Deployment

### Local Deployment (Current Setup)
- Run all components on your machine
- No cloud costs
- Full data privacy
- Requires local GPU for faster inference (optional)

### Production Deployment Ideas
- **Docker Containerization** — Package entire stack in containers
- **Cloud Instances** — Deploy on AWS EC2, Azure VM, or Google Cloud
- **Kubernetes** — Orchestrate multiple instances
- **API Server** — Use Gunicorn/uWSGI instead of uvicorn for production
- **Frontend Hosting** — Deploy Streamlit on Streamlit Cloud

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) file for details.

---

## 📚 References

- [IPCC AR6 Reports](https://www.ipcc.ch/reports/ar6-synthesis-report/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Models](https://ollama.ai/library)
- [Chroma Vector DB](https://www.trychroma.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)

---

## 👨‍💻 Author

Created as a demonstration of RAG systems applied to scientific document analysis.

---

## ⚠️ Disclaimer

This system uses local LLMs which may generate inaccurate information. Always verify critical climate information with official IPCC reports at [ipcc.ch](https://www.ipcc.ch/). This is a research/educational project.

---

