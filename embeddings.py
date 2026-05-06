# embeddings.py
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json, os

def embed_and_store(chunks_dir="chunks", persist_directory="vectordb"):
    print("🔧 Initialisation des embeddings Ollama...")
    embedder = OllamaEmbeddings(model="nomic-embed-text:latest")
    
    documents = []
    for fn in os.listdir(chunks_dir):
        if not fn.endswith(".json"):
            continue
        filepath = os.path.join(chunks_dir, fn)
        with open(filepath, "r", encoding="utf8") as f:
            items = json.load(f)
        for it in items:
            documents.append(
                Document(
                    page_content=it["page_content"],
                    metadata=it.get("metadata", {})
                )
            )
    
    print(f"📦 {len(documents)} chunks à vectoriser...")
    
    vectordb = Chroma.from_documents(
        documents,
        embedding=embedder,
        persist_directory=persist_directory
    )
    vectordb.persist()
    print(f"✅ Vector DB sauvegardée dans '{persist_directory}/'")
    return vectordb

if __name__ == "__main__":
    embed_and_store()