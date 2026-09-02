import pickle
from pathlib import Path
import faiss


class FaissStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embeddings, metadata):
        self.index.add(embeddings.astype("float32"))
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k=5):
        scores, idxs = self.index.search(query_embedding.astype("float32"), top_k)
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx != -1:
                results.append({"score": float(score), "metadata": self.metadata[idx]})

        return results

    def save(self, index_path, meta_path):
        Path(index_path).parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(index_path))
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)