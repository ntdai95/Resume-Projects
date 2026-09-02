from pathlib import Path
from datetime import datetime, timezone
import math
import joblib
import mlflow
import mlflow.xgboost
import pandas as pd
import yaml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from app.core.settings import settings


def train_xgboost_from_parquet(parquet_path: str, model_out: str, config_path: str = "configs/model_config.yaml"):
    settings.ensure_dirs()
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    df = pd.read_parquet(parquet_path)
    if "time_ts" in df.columns:
        df["time_ts"] = pd.to_datetime(df["time_ts"], errors="coerce")
        sort_cols = ["time_ts"]
        if "dataset_id" in df.columns:
            sort_cols = ["dataset_id", "time_ts"]

        df = df.sort_values(sort_cols).reset_index(drop=True)

    target = cfg["forecasting"]["target_variable"]
    drop_cols = [target, "source_variable", "canonical_variable", "units", "normalized_unit", "source_file",
                 "dataset_id", "provenance_transform", "time_ts", "time", "value", "row", "latitude", "longitude"]

    feature_cols = [c for c in df.columns if c not in drop_cols]
    X = df[feature_cols]
    y = df[target]
    split = int(len(df) * (1 - cfg["forecasting"]["test_fraction"]))
    X_train = X.iloc[:split]
    X_test = X.iloc[split:]
    y_train = y.iloc[:split]
    y_test = y.iloc[split:]
    params = cfg["xgboost"]
    model = XGBRegressor(**params)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)
    with mlflow.start_run(run_name="train_baseline_xgboost"):
        mlflow.log_params(params)
        mlflow.log_param("train_rows", len(X_train))
        mlflow.log_param("test_rows", len(X_test))
        mlflow.log_param("feature_count", len(feature_cols))
        mlflow.log_param("split_strategy", "chronological_holdout")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = math.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        metrics = {"rmse": float(rmse), "mae": float(mae), "r2": float(r2)}
        mlflow.log_metrics(metrics)
        feature_importance = dict(zip(feature_cols, model.feature_importances_.tolist()))
        model_package = {"model": model, "feature_cols": feature_cols, "metrics": metrics,
                         "trained_at": datetime.now(timezone.utc).isoformat()}

        Path(model_out).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model_package, model_out)
        mlflow.xgboost.log_model(model, artifact_path="model")

    details = {"feature_cols": feature_cols, "feature_importance": feature_importance, "y_test": y_test.tolist(),
               "preds": preds.tolist()}
    
    return metrics, details