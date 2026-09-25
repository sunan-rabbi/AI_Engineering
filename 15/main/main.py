import json
import os
import qdrant_setup as qdrant_db

from qdrant_client.models import Filter, FieldCondition, MatchValue # type: ignore
from embedding_setup import get_embedding # type: ignore
from groq_setup import ask_llm # type: ignore



# 1. Load documents
# base_dir = os.path.dirname(os.path.abspath(__file__))
# knowledge_path = os.path.join(base_dir, "video.json")

# with open(knowledge_path, "r", encoding="utf-8") as f:
#     documents = json.load(f)



# 2. Setup collection & upload
# print("Setting up Qdrant collection...")
# qdrant_db.init_collection()



# 3. Upload documents with embeddings
# texts = [doc["text"] for doc in documents]
# embeddings = get_embedding(texts)
# qdrant_db.upload_documents(documents, embeddings)
# print("Uploaded successfully!")



# 4. user query and search
query = "explain the data structures."
query_vec = get_embedding(query)
results = qdrant_db.search(query_vec, top_k=3)



# 5. Display results and prepare context for LLM
context = []
print("\nFiltered Search Results:")
for r in results:
    context.append({
        "text": r.payload["text"],
        "video_name": r.payload["video_name"],
        "start_time": r.payload["start_time"],
        "end_time": r.payload["end_time"],
        "timestamp": r.payload["timestamp"]
    })
print(json.dumps(context, indent=2))



# 6. Ask LLM for final answer
answer = ask_llm(query, context)
print("\nFinal Answer:")
print()
print(answer)