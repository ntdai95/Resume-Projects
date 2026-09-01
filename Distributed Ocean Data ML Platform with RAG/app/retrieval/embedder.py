import torch


class Embedder:
    def __init__(self, model_name):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        
    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True)
