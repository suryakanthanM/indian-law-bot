from app.services.vector_db import search_db
import time

start = time.time()
print("Searching...")
try:
    results = search_db("traffic laws", 3)
    print("Found docs:", len(results.get('documents', [[]])[0]))
except Exception as e:
    print("Error:", e)
print("Time taken:", time.time() - start)
