from pathlib import Path
from datetime import datetime
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
    target = cfg["forecasting"]["target_variable"]
    drop_cols = [
        target,
        "source_variable",
        "canonical_variable",
        "units",
        "normalized_unit",
        "source_file",
        "dataset_id",
        "provenance_transform",
        "time_ts",
    ]

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
        mlflow.log_param("num_features", len(feature_cols))
        mlflow.log_param("dataset_path", parquet_path)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = float(mean_absolute_error(y_test, preds))
        rmse = float(math.sqrt(mean_squared_error(y_test, preds)))
        r2 = float(r2_score(y_test, preds))
        metrics = {
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
        }

        mlflow.log_metrics(metrics)
        mlflow.xgboost.log_model(model, "model")
        Path(model_out).parent.mkdir(parents=True, exist_ok=True)
        model_package = {
            "model": model,
            "features": feature_cols,
            "training_time": datetime.utcnow().isoformat(),
            "dataset": str(parquet_path),
            "params": params,
            "metrics": metrics,
        }

        joblib.dump(model_package, model_out)
        mlflow.log_artifact(model_out)

    details = {
        "y_test": y_test.tolist(),
        "preds": preds.tolist(),
        "feature_cols": feature_cols,
        "feature_importance": dict(
            zip(feature_cols, model.feature_importances_.tolist())
        ),
    }

    return metrics, details