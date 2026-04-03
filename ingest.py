import os
import glob
from app.utils.pdf_processor import extract_and_chunk_pdf
from app.services.vector_db import add_to_db

print("Starting custom ingestion script...")
raw_folder = "./data/raw"
total_chunks = 0
files_processed = []

if not os.path.exists(raw_folder):
    print("No raw folder.")
    exit(1)

for file_path in glob.glob(os.path.join(raw_folder, "*.pdf")):
    filename = os.path.basename(file_path)
    print(f"Processing {filename}...")
    
    chunks = extract_and_chunk_pdf(file_path)
    print(f"Extracted {len(chunks)} chunks.")
    
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename} for _ in range(len(chunks))]
    
    # Process in batches to prevent SQLite crashes on huge inserts
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        b_chunks = chunks[i:i+batch_size]
        b_metas  = metadatas[i:i+batch_size]
        b_ids    = ids[i:i+batch_size]
        print(f"Adding batch {i//batch_size + 1}...")
        add_to_db(documents=b_chunks, metadatas=b_metas, ids=b_ids)
        
    total_chunks += len(chunks)
    files_processed.append(filename)

print("Finished!", total_chunks, "chunks total.")
