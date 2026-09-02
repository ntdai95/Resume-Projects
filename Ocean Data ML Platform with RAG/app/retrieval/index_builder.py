from app.retrieval.chunker import chunk_text
from app.retrieval.vector_store_faiss import FaissStore
from app.retrieval.vector_store_qdrant import QdrantStore
from app.core.settings import settings


def build_index(docs, model_name):
    from app.retrieval.embedder import Embedder
    texts, meta = [], []
    for doc in docs:
        for i, chunk in enumerate(chunk_text(doc["text"])):
            texts.append(chunk)
            meta.append({**doc, "chunk_id": f'{doc["doc_id"]}:{i}', "text": chunk})

    embeddings = Embedder(model_name).encode(texts)
    if settings.vector_backend == "qdrant":
        store = QdrantStore(dim=embeddings.shape[1])
        store.add(embeddings, meta)
        return store
    
    store = FaissStore(dim=embeddings.shape[1])
    store.add(embeddings, meta)
    store.save("data/index/faiss.index", "data/index/faiss_meta.pkl")
    return store
