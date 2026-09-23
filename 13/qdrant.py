# Import
import os
from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore
import numpy as np # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.models import Distance, VectorParams, PointStruct # type: ignore


# Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if not my_api_key or not qdrant_api_key or not qdrant_url:
    raise ValueError("GROQ_API_KEY environment variable is not set.")


# Client and Models
groqClient = Groq(api_key=my_api_key)

qdrantClient = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

AImodel = "openai/gpt-oss-120b"
EMmodel=SentenceTransformer('all-MiniLM-L6-v2')


# Qdrant Collection Create
COLLECTION='knowledge'
SIZE= 384

if qdrantClient.collection_exists(COLLECTION):
    qdrantClient.delete_collection(COLLECTION)

qdrantClient.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(
        size=SIZE,
        distance=Distance.COSINE
    )
)


# Load information in Vector DB
docs=[
    'Employees receive 24 days of paid leave per year.',
    'Employees work from the office on Tuesday, Wednesday and Thursday. Monday and Friday are optional work-from-home days.',
    'Employees receive TK 3000 per month for gym reimbursement.',
    'Employees can claim TK 2000 per month for home internet.',
    'Employees have a 90 day notice period.'
]

docsEmbed=EMmodel.encode(docs)

points = []

for i, embedding in enumerate(docsEmbed):
    point = PointStruct(
        id=i+1,
        vector=embedding.tolist(),
        payload={'text':docs[i]}
    )
    points.append(point)

qdrantClient.upsert(
    collection_name=COLLECTION,
    points=points
)


# Helper function
def search(query, top=3):

    queryVector = EMmodel.encode(query).tolist()

    results = qdrantClient.query_points(
        collection_name=COLLECTION,
        query=queryVector,
        limit=top,
        with_payload=True
    ).points

    return results


def ask_llm(question,context):
 
    sys_msg={
         "role":"system",
         "content":f"Answer in short or one line , answer only based on this content. don't hallucinate, context: {context}"
    }

    user_msg={
         "role":"user",
         "content":question
    }

    messages=[sys_msg,user_msg]

    response = groqClient.chat.completions.create(model=AImodel,messages=messages)

    answer = response.choices[0].message.content

    return answer


query = 'How many vacation days do I get?'

results = search(query)
context = '\n'.join(result.payload['text'] for result in results)

answer = ask_llm(query,context)

print()
print(answer)
