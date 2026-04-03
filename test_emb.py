import urllib.request
import json
import time

api_key = "AIzaSyA41pgyH2qyPl-fbed8PiVVMeBeIFoiWkM"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={api_key}"
payload = {
    "model": "models/gemini-embedding-001",
    "content": {"parts": [{"text": "Hello world"}]}
}
req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

start = time.time()
try:
    with urllib.request.urlopen(req, timeout=5) as response:
        print(response.status)
        data = json.loads(response.read().decode('utf-8'))
        print("Got embedding of len", len(data["embedding"]["values"]))
except Exception as e:
    print("Error:", e)
print("Time taken:", time.time() - start)
