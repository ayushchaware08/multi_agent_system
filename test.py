# import os
# print("Groq key loaded:", os.getenv("GROQ_API_KEY"))
import requests
import json

url = "http://localhost:8000/ask/"
payload = {"text": "test query"}

print("🔍 Sending request to:", url)
print("📦 Payload:", payload)

try:
    response = requests.post(url, json=payload, timeout=60)
    print("\n✅ Status Code:", response.status_code)
    print("📄 Response:")
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.Timeout:
    print("❌ Request timed out after 60 seconds")
except Exception as e:
    print(f"❌ Error: {e}")
