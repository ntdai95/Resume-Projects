import faiss, numpy as pickle
from pathlib import Path


class FaissStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embeddings, metadata):
        self.index.add(embeddings.astype("float32"))
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k=5):
        scores, idxs = self.index.search(query_embedding.astype("float32"), top_k)
        return [{"score": float(score), "metadata": self.metadata[idx]} for score, idx in zip(scores[0], idxs[0]) if idx != -1]
    
    def save(self, index_path, meta_path):
        Path(index_path).parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(index_path))
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
