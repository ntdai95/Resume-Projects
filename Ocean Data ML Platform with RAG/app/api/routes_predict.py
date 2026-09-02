from pathlib import Path
import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.settings import settings


router = APIRouter(tags=["prediction"])


class PredictRequest(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    dayofyear: int = Field(..., ge=1, le=366)
    lag_1: float
    lag_3: float
    lag_6: float


def _load_model_package():
    tuned_path = settings.artifacts_dir / "models" / "temperature_forecaster_tuned.joblib"
    baseline_path = Path(settings.model_path)
    model_path = tuned_path if tuned_path.exists() else baseline_path
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Model file not found. Run training first.")

    package = joblib.load(model_path)
    if not isinstance(package, dict) or "model" not in package:
        raise HTTPException(status_code=500, detail="Invalid model package format.")

    return package


@router.post("/predict")
def predict(payload: PredictRequest):
    package = _load_model_package()
    model = package["model"]
    feature_cols = package.get("feature_cols") or package.get("features")
    if not feature_cols:
        raise HTTPException(status_code=500, detail="Model package missing feature columns.")

    input_values = {"hour": payload.hour, "dayofyear": payload.dayofyear, "lag_1": payload.lag_1,
                    "lag_3": payload.lag_3, "lag_6": payload.lag_6}

    row = {col: input_values.get(col, 0) for col in feature_cols}
    X = pd.DataFrame([row], columns=feature_cols)
    prediction = model.predict(X)[0]
    return {"prediction": float(prediction), "target": "sea_water_temperature", "unit": "degC", 
            "features_used": feature_cols, "input": input_values, "model_metrics": package.get("metrics", {})}