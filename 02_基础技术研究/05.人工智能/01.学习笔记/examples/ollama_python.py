import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2:3b",
    "prompt": "请用一句话解释什么是操作系统。",
    "stream": False
}

response = requests.post(url, json=payload)
result = response.json()

print(result["response"])
