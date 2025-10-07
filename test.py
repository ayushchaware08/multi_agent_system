# import os
# print("Groq key loaded:", os.getenv("GROQ_API_KEY"))

#  test backend
# import requests
# import json

# url = "http://localhost:8000/ask/"
# payload = {"text": "test query"}

# print("🔍 Sending request to:", url)
# print("📦 Payload:", payload)

# try:
#     response = requests.post(url, json=payload, timeout=60)
#     print("\n✅ Status Code:", response.status_code)
#     print("📄 Response:")
#     print(json.dumps(response.json(), indent=2))
# except requests.exceptions.Timeout:
#     print("❌ Request timed out after 60 seconds")
# except Exception as e:
#     print(f"❌ Error: {e}")

# test embeddings
# import logging
# logging.basicConfig(level=logging.INFO)

# from langchain_huggingface import HuggingFaceEmbeddings

# print("Loading model...")
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )
# print("Model loaded!")

# print("Testing embedding...")
# result = embeddings.embed_query("test")
# print(f"Embedding dimension: {len(result)}")
# print("Success!")


from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
import time

class SimpleEmbeddings:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=False).tolist()
    
    def embed_query(self, text):
        return self.model.encode([text], show_progress_bar=False)[0].tolist()

print("Creating vectorstore...")
embeddings = SimpleEmbeddings()
vectorstore = Chroma(collection_name="test", embedding_function=embeddings)

print("Adding document...")
start = time.time()
docs = [Document(page_content="test", metadata={"id": 1})]
vectorstore.add_documents(docs)
print(f"✅ Done in {time.time() - start:.2f}s")
