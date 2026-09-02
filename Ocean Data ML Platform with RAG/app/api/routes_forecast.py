import json
from fastapi import APIRouter
from app.core.settings import settings


router = APIRouter()

@router.get("/forecast")
def forecast():
    if not settings.metrics_report_path.exists():
        return {"message": "Run model evaluation first to generate forecasting metrics."}

    payload = json.loads(settings.metrics_report_path.read_text())
    return {
        "message": "Forecasting model artifacts available",
        "metrics": payload,
        "model_path": str(settings.model_path),
    }