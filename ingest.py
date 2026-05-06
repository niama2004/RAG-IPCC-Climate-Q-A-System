# ingest.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os, glob, json

def load_and_split(pdf_path, chunk_size=1000, chunk_overlap=200):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

def main():
    os.makedirs("chunks", exist_ok=True)
    pdf_files = glob.glob("data/*.pdf")
    
    if not pdf_files:
        print("❌ Aucun PDF trouvé dans data/")
        return
    
    for p in pdf_files:
        print(f"📄 Processing: {p}")
        docs = load_and_split(p)
        out = [{"page_content": d.page_content, "metadata": d.metadata} for d in docs]
        fn = os.path.join("chunks", os.path.basename(p) + ".json")
        with open(fn, "w", encoding="utf8") as f:
            json.dump(out, f, ensure_ascii=False)
        print(f"✅ Saved {len(docs)} chunks → {fn}")

if __name__ == "__main__":
    main()