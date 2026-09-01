from pathlib import Path
import jsonlines
from app.core.settings import settings


def load_docs():
    docs = []
    manifest_path = Path("data/manifests/source_manifest.jsonl")
    if manifest_path.exists():
        with jsonlines.open(manifest_path) as reader:
            for row in reader:
                text = (
                    f"Dataset {row.get('dataset_id', 'unknown')} from file {row.get('file_path', 'unknown')}. "
                    f"Variables: {', '.join(row.get('variables', []))}. "
                    f"Coordinates: {', '.join(row.get('coordinates', []))}. "
                    f"Attributes: {row.get('attrs', {})}"
                )

                docs.append(
                    {
                        "doc_id": row.get("sha256", row.get("file_path", "unknown")),
                        "dataset_id": row.get("dataset_id", "unknown"),
                        "source_file": row.get("file_path", "unknown"),
                        "variable": ",".join(row.get("variables", [])),
                        "text": text,
                    }
                )

    metrics_path = Path(settings.metrics_report_path)
    if metrics_path.exists():
        docs.append(
            {
                "doc_id": "model-metrics",
                "dataset_id": "model",
                "source_file": str(metrics_path),
                "variable": "",
                "text": "Model metrics: " + metrics_path.read_text(),
            }
        )

    return docs


def ensure_rag_ready(app):
    if getattr(app.state, "retriever", None) is not None and getattr(app.state, "answerer", None) is not None:
        return

    docs = load_docs()
    if not docs:
        app.state.retriever = None
        app.state.answerer = None
        return

    from app.retrieval.index_builder import build_index
    from app.retrieval.retriever import Retriever
    from app.rag.llm_client import LLMClient
    from app.rag.answerer import RAGAnswerer

    store = build_index(docs, settings.embedding_model)
    app.state.retriever = Retriever(store, settings.embedding_model)
    app.state.answerer = RAGAnswerer(app.state.retriever, LLMClient())