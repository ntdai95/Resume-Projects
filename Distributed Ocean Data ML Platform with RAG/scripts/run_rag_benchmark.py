import json
import torch
from sentence_transformers import SentenceTransformer
from app.core.settings import settings
from app.rag.evaluation import evaluate_retriever, save_retrieval_eval
from app.rag.runtime import load_docs
from app.retrieval.index_builder import build_index
from app.retrieval.retriever import Retriever


def main():
    settings.ensure_dirs()
    docs = load_docs()
    if not docs:
        raise RuntimeError("No documents found. Run extract_manifest first.")

    store = build_index(docs, settings.embedding_model)
    retriever = Retriever(store, settings.embedding_model)
    summary = evaluate_retriever(retriever, top_k=settings.rag_eval_top_k)
    artifacts = save_retrieval_eval(summary)
    print(json.dumps(
        {
            "message": "Retrieval benchmark completed",
            "metrics": summary["metrics"],
            "num_queries": summary["num_queries"],
            "artifacts": artifacts,
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()