from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.core.settings import settings


class QdrantStore:
    def __init__(self, dim, collection_name=None):
        self.collection_name = collection_name or settings.qdrant_collection
        self.client = QdrantClient(url=settings.qdrant_url)
        self.client.recreate_collection(collection_name=self.collection_name, vectors_config=VectorParams(size=dim, distance=Distance.COSINE))
    
    def add(self, embeddings, metadata):
        points = [PointStruct(id=i, vector=vec.tolist(), payload=meta) for i, (vec, meta) in enumerate(zip(embeddings, metadata))]
        self.client.upsert(collection_name=self.collection_name, points=points)
    
    def search(self, query_embedding, top_k=5):
        hits = self.client.search(collection_name=self.collection_name, query_vector=query_embedding[0].tolist(), limit=top_k)
        return [{"score": float(h.score), "metadata": h.payload} for h in hits]
