import requests

res = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": "What is the stock market?",
    "stream": False
})

print(res.json())
