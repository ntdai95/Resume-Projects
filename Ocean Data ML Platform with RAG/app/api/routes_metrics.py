import json
import joblib
from fastapi import APIRouter
from app.core.settings import settings


router = APIRouter()

@router.get("/metrics")
def metrics():
    baseline_metrics = {}
    tuned_metrics = {}
    rag_metrics = {}
    if settings.metrics_report_path.exists():
        baseline_metrics = json.loads(settings.metrics_report_path.read_text())

    tuned_path = settings.artifacts_dir / "models" / "temperature_forecaster_tuned.joblib"
    if tuned_path.exists():
        tuned_metrics = joblib.load(tuned_path).get("metrics", {})

    if settings.rag_eval_report_path.exists():
        rag_metrics = json.loads(settings.rag_eval_report_path.read_text())

    if not baseline_metrics and not tuned_metrics and not rag_metrics:
        return {"message": "No metrics found. Run evaluation scripts first."}

    return {"forecasting": {"baseline": baseline_metrics, "tuned": tuned_metrics}, "retrieval": rag_metrics}