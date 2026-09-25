import os
from dotenv import load_dotenv # type: ignore
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.models import ( # type: ignore
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
)

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "knowledge_filter"
EMBEDDING_SIZE = 384



def init_collection():
    """Recreates the collection and adds payload indexes."""
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_SIZE,
            distance=Distance.COSINE,
        ),
    )


def upload_documents(documents, embeddings):
    """Uploads documents along with their pre-computed vectors."""
    points = [
        PointStruct(
            id=i + 1,
            vector=embeddings[i],
            payload=documents[i],
        )
        for i in range(len(documents))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)


def search(query_vector, query_filter=None, top_k=3):
    """Searches Qdrant with an embedded query vector."""
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=query_filter,
    ).points
    return results