import ast
from pathlib import Path
import jsonlines
from app.core.settings import settings

USEFUL_ATTRS = ["device_name", "time_coverage_start", "time_coverage_end", "DOI"]


def _parse_attrs(raw):
    try:
        return ast.literal_eval(raw) if raw else {}
    except (ValueError, SyntaxError):
        return {}


def load_docs():
    docs = []
    manifest_path = Path("data/manifests/source_manifest.jsonl")
    if manifest_path.exists():
        with jsonlines.open(manifest_path) as reader:
            for row in reader:
                variables = row.get("variables", "")
                attrs = _parse_attrs(row.get("attrs", ""))

                sentences = [
                    f"Dataset {row.get('dataset_id', 'unknown')} from file {row.get('file_path', 'unknown')}, "
                    f"measuring {variables.replace(',', ', ')}."
                ]
                for key in USEFUL_ATTRS:
                    if attrs.get(key):
                        sentences.append(f"{key.replace('_', ' ').title()}: {attrs[key]}.")
                text = " ".join(sentences)

                docs.append(
                    {
                        "doc_id": row.get("sha256", row.get("file_path", "unknown")),
                        "dataset_id": row.get("dataset_id", "unknown"),
                        "source_file": row.get("file_path", "unknown"),
                        "variable": variables,
                        "text": text,
                    }
                )

    report_docs = [
        ("model-metrics", settings.metrics_report_path, "Baseline XGBoost water temperature forecasting model metrics"),
        ("hyperparameter-search", settings.artifacts_dir / "reports" / "hyperparameter_search.json", "Optuna hyperparameter search results for the tuned XGBoost water temperature model"),
        ("horizon-experiment", settings.horizon_report_path, "Persistence baseline vs. XGBoost forecast error across horizons, with and without cross-sensor context, for ocean water temperature"),
        ("air-temperature-benchmark", settings.air_temp_report_path, "Persistence baseline vs. XGBoost forecast error across horizons, with and without pressure and wind context, for air temperature"),
    ]
    for doc_id, path, description in report_docs:
        path = Path(path)
        if path.exists():
            docs.append(
                {
                    "doc_id": doc_id,
                    "dataset_id": "model",
                    "source_file": str(path),
                    "variable": "",
                    "text": f"{description}: {path.read_text()}",
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