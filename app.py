# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma


from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

app = FastAPI(title="RAG IPCC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement de la base vectorielle
embedding_fn = OllamaEmbeddings(model="nomic-embed-text:latest")
vectordb = Chroma(persist_directory="vectordb", embedding_function=embedding_fn)
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# LLM — adapte le model selon ce que tu as pull
llm = ChatOllama(model="llama3.2:3b", temperature=0.0)

prompt = PromptTemplate.from_template(
    """Use the following context from IPCC AR6 reports to answer the question.
If the answer is not in the context, say 'I don't know based on the provided documents.'

Context:
{context}

Question: {question}

Answer:"""
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Ajoute ces lignes AVANT le @app.post("/ask")
from pydantic import BaseModel

class QueryIn(BaseModel):
    question: str

@app.post("/ask")
def ask(q: QueryIn):
    docs = docs = retriever.invoke(q.question)
    answer = rag_chain.invoke(q.question)
    sources = [
        {
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", "?"),
            "preview": doc.page_content[:200] + "..."
        }
        for doc in docs
    ]
    return {"answer": answer, "sources": sources}


@app.get("/")
def root():
    return {"status": "RAG IPCC API is running ✅"}