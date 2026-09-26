import json
import os
import qdrant_setup as qdrant_db

from qdrant_client.models import Filter, FieldCondition, MatchValue # type: ignore
from embedding_setup import get_embedding # type: ignore
from groq_setup import ask_llm # type: ignore



# 1. Load documents
base_dir = os.path.dirname(os.path.abspath(__file__))
knowledge_path = os.path.join(base_dir, "knowledge.json")

with open(knowledge_path, "r", encoding="utf-8") as f:
    documents = json.load(f)

# 2. Setup collection & upload
print("Setting up Qdrant collection...")
qdrant_db.init_collection()


texts = [doc["text"] for doc in documents]
embeddings = get_embedding(texts)
qdrant_db.upload_documents(documents, embeddings)
print("Uploaded successfully!")


query = "How many vacation days I will get in a year"
EMquery = get_embedding(query)


# 4. End-to-End RAG Pipeline
results = qdrant_db.search(EMquery, top_k=3)

context = "\n".join(r.payload["text"] for r in results)
answer = ask_llm(query, context)

print("\nFinal Answer:")
print(answer)