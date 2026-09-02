import json
from dataclasses import asdict, dataclass
from app.core.settings import settings
from app.ml.experiment_tracker import log_run


@dataclass
class RetrievalEvalExample:
    question: str
    relevant_terms: list[str]


@dataclass
class RetrievalEvalRow:
    question: str
    hit_at_k: int
    term_recall: float
    matched_terms: list[str]
    returned_doc_ids: list[str]
    returned_dataset_ids: list[str]


def default_eval_set():
    return [
        RetrievalEvalExample(
            question="Which Ocean Networks Canada sensor recorded the water's temperature?",
            relevant_terms=["onc", "temperature"],
        ),
        RetrievalEvalExample(
            question="Which NOAA dataset holds sea surface temperature readings?",
            relevant_terms=["noaa", "temp"],
        ),
        RetrievalEvalExample(
            question="What variable would show whether the seawater is getting saltier?",
            relevant_terms=["salinity"],
        ),
        RetrievalEvalExample(
            question="Which sensor tracks how much oxygen is dissolved in the water?",
            relevant_terms=["oxygen"],
        ),
        RetrievalEvalExample(
            question="Is there a file that records barometric or water pressure readings?",
            relevant_terms=["pressure"],
        ),
        RetrievalEvalExample(
            question="Which file has wind speed measurements?",
            relevant_terms=["wind"],
        ),
        RetrievalEvalExample(
            question="How accurate is the trained temperature forecasting model?",
            relevant_terms=["rmse", "r2"],
        ),
        RetrievalEvalExample(
            question="What hyperparameters did the Optuna search settle on for the tuned model?",
            relevant_terms=["best_params"],
        ),
        RetrievalEvalExample(
            question="Does forecasting skill for ocean water temperature change at longer time horizons?",
            relevant_terms=["horizon_seconds"],
        ),
        RetrievalEvalExample(
            question="Is air temperature more predictable than water temperature at longer horizons?",
            relevant_terms=["horizon_minutes"],
        ),
    ]


def _normalize(text):
    return " ".join(text.lower().split())


def evaluate_retriever(retriever, examples=None, top_k=None):
    examples = examples or default_eval_set()
    top_k = top_k or settings.rag_eval_top_k
    rows: list[RetrievalEvalRow] = []
    for example in examples:
        results = retriever.retrieve(example.question, top_k=top_k)
        matched_terms = set()
        returned_doc_ids = []
        returned_dataset_ids = []
        hit_at_k = 0
        for row in results:
            text = _normalize(row.get("text", ""))
            returned_doc_ids.append(str(row.get("doc_id", "")))
            returned_dataset_ids.append(str(row.get("dataset_id", "")))
            row_matched = False
            for term in example.relevant_terms:
                if _normalize(term) in text:
                    matched_terms.add(term)
                    row_matched = True

            if row_matched:
                hit_at_k = 1

        recall = 0.0
        if example.relevant_terms:
            recall = len(matched_terms) / len(set(example.relevant_terms))

        rows.append(
            RetrievalEvalRow(
                question=example.question,
                hit_at_k=hit_at_k,
                term_recall=recall,
                matched_terms=sorted(matched_terms),
                returned_doc_ids=returned_doc_ids,
                returned_dataset_ids=returned_dataset_ids,
            )
        )

    hit_at_k = sum(r.hit_at_k for r in rows) / max(len(rows), 1)
    term_recall = sum(r.term_recall for r in rows) / max(len(rows), 1)
    summary = {
        "num_queries": len(rows),
        "top_k": top_k,
        "metrics": {"hit_at_k": hit_at_k, "term_recall": term_recall},
        "rows": [asdict(r) for r in rows],
    }

    return summary


def save_retrieval_eval(summary):
    settings.ensure_dirs()
    summary_copy = dict(summary)
    rows = summary_copy.pop("rows", [])
    settings.rag_eval_report_path.write_text(json.dumps(summary_copy, indent=2), encoding="utf-8")
    with settings.rag_eval_rows_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    log_run(
        run_name="retrieval_eval",
        params={"top_k": summary.get("top_k"), "num_queries": summary.get("num_queries")},
        metrics=summary.get("metrics", {}),
        experiment_name=settings.mlflow_rag_experiment_name,
    )

    return {"summary_path": str(settings.rag_eval_report_path), "rows_path": str(settings.rag_eval_rows_path)}