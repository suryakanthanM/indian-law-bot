import urllib.request
import time
import json

url = "http://127.0.0.1:8000/ask?question=traffic"
start = time.time()
try:
    req = urllib.request.Request(url, method='POST')
    # Since the API expects an invalid accept header in frontend maybe? 
    # Frontend sends POST with no body.
    response = urllib.request.urlopen(req, timeout=10)
    print("Status:", response.status)
    print("Body:", response.read().decode())
except Exception as e:
    print("Error:", e)
print("Time taken:", time.time() - start)
