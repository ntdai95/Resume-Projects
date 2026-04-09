import json
from fastapi import APIRouter
from app.core.settings import settings


router = APIRouter()

@router.get("/metrics")
def metrics():
    model_metrics = {}
    rag_metrics = {}
    if settings.metrics_report_path.exists():
        model_metrics = json.loads(settings.metrics_report_path.read_text())

    if settings.rag_eval_report_path.exists():
        rag_metrics = json.loads(settings.rag_eval_report_path.read_text())

    if not model_metrics and not rag_metrics:
        return {"message": "No metrics found. Run evaluation scripts first."}

    return {"forecasting": model_metrics, "retrieval": rag_metrics}