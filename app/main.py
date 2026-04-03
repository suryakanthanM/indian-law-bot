import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.ai_service import get_ai_response
# NEW: Import your processor and database functions
from app.utils.pdf_processor import extract_and_chunk_pdf
from app.services.vector_db import add_to_db, search_db 

app = FastAPI(
    title="Indian Law Bot API",
    description="AI-powered legal assistant for Indian Law"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online", "message": "Welcome to the Indian Law Bot API!"}

@app.get("/test-ai")
async def test_ai(question: str):
    answer = get_ai_response(question)
    return {"question": question, "answer": answer}

# NEW: Route to process your PDFs
@app.post("/ingest")
async def ingest_pdfs():
    """Reads all PDFs in the data/raw folder and adds them to ChromaDB."""
    raw_folder = "./data/raw"
    total_chunks = 0
    files_processed = []

    # 1. Check if the folder exists
    if not os.path.exists(raw_folder):
        return {"error": f"Folder {raw_folder} does not exist."}

    # 2. Loop through every file in the folder
    for filename in os.listdir(raw_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(raw_folder, filename)
            
            # 3. Extract and chunk the PDF
            chunks = extract_and_chunk_pdf(file_path)
            
            # 4. Prepare data for ChromaDB
            # We need to give each chunk a unique ID and store the source filename
            ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{"source": filename} for _ in range(len(chunks))]
            
            # 5. Save to database
            add_to_db(documents=chunks, metadatas=metadatas, ids=ids)
            
            total_chunks += len(chunks)
            files_processed.append(filename)

    return {
        "message": "Ingestion complete!",
        "files_processed": files_processed,
        "total_chunks_added": total_chunks
    }

@app.post("/ask")
async def ask_legal_bot(question: str):
    """Answers a legal question using the uploaded PDFs."""
    
    # 1. Search the database for the top 3 most relevant law chunks
    search_results = search_db(query=question, n_results=3)
    
    # Check if the database returned anything
    if not search_results['documents'] or not search_results['documents'][0]:
        return {"answer": "I haven't ingested any laws related to that yet!"}
        
    # 2. Extract the actual text and source data
    context_chunks = search_results['documents'][0]
    source_metadata = search_results['metadatas'][0]
    
    # Combine the chunks into one big string of legal text
    legal_context = "\n\n--- Next Excerpt ---\n\n".join(context_chunks)
    
    # 3. Build the strict Prompt for Gemini
    prompt = f"""
    You are an expert Indian Legal Assistant. 
    You must answer the user's question using ONLY the following legal excerpts.
    If the answer is not in the text, say "I cannot answer this based on the provided documents."
    Do not guess or use outside knowledge. 
    Always provide your final response in both English and Tamil.
    Cite the specific rules/sections from the text.

    LEGAL EXCERPTS:
    {legal_context}

    USER QUESTION:
    {question}
    """
    
    # 4. Ask Gemini
    answer = get_ai_response(prompt)
    
    # 5. Return the answer AND the sources used so the user can verify
    return {
        "question": question,
        "answer": answer,
        "sources_used": source_metadata
    }