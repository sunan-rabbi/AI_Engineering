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

# 3. Optional Filter Demo
reimbursement_filter = Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="reimbursement"),
        ),
        FieldCondition(
            key="is_active",
            match=MatchValue(value="true"),
        ),
    ]
)

test_query = "is there any allowance for physical activity?"
query_vec = get_embedding(test_query)
filtered_results = qdrant_db.search(query_vec, query_filter=reimbursement_filter, top_k=3)

print("\nFiltered Search Results:")
for r in filtered_results:
    print(f"Score: {r.score:.3f} | {r.payload['text']}")


# 4. End-to-End RAG Pipeline
results = qdrant_db.search(query_vec, top_k=3)

context = "\n".join(r.payload["text"] for r in results)
answer = ask_llm(test_query, context)

print("\nFinal Answer:")
print(answer)