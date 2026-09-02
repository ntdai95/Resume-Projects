import numpy as np
from app.retrieval.embedder import Embedder


class Retriever:
    def __init__(self, store, model_name):
        self.store = store
        self.embedder = Embedder(model_name)

    def retrieve(self, query, top_k=5):
        q = self.embedder.encode([query])
        results = self.store.search(np.asarray(q), top_k=top_k)
        normalized = []
        for row in results:
            metadata = row.get("metadata", {}) or {}
            normalized.append(
                {
                    "score": float(row.get("score", 0.0)),
                    "doc_id": metadata.get("doc_id"),
                    "dataset_id": metadata.get("dataset_id"),
                    "source_file": metadata.get("source_file"),
                    "variable": metadata.get("variable"),
                    "chunk_id": metadata.get("chunk_id"),
                    "text": metadata.get("text", ""),
                    "metadata": metadata,
                }
            )

        return normalized