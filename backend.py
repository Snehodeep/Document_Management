
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import pipeline
import chromadb

app = FastAPI(title="Document Ingestion and Q&A API")

# Initialize embeddings and LLM
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
generator = pipeline("text2text-generation", model="google/flan-t5-base")
llm = HuggingFacePipeline(pipeline=generator)

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Pydantic models for request validation
class DocumentRequest(BaseModel):
    content: str

class QuestionRequest(BaseModel):
    question: str

def get_db():
    """Get or create Chroma database instance."""
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_name="my_documents"
    )

@app.post("/ingest")
async def ingest_document(request: DocumentRequest):
    """Ingest a document, split it, generate embeddings, and store in Chroma."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(request.content)
        db = get_db()
        db.add_texts(texts, metadatas=[{"source": "uploaded_document"}] * len(texts))
        db.persist()
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/qa")
async def get_answer(request: QuestionRequest):
    """Answer a question using RAG with retrieved documents."""
    try:
        db = get_db()
        retriever = db.as_retriever(search_kwargs={"k": 4})
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        result = qa({"query": request.question})
        return {
            "answer": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Q&A failed: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List all documents in the database."""
    db = get_db()
    documents = db.get()
    return {"documents": documents["metadatas"]}
