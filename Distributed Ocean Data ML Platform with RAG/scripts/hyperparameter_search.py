import json
from pathlib import Path
import joblib
import mlflow
import optuna
import pandas as pd
import yaml
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from xgboost import XGBRegressor
from app.core.settings import settings


def load_config(config_path="configs/model_config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def prepare_data(parquet_path, config_path="configs/model_config.yaml"):
    cfg = load_config(config_path)
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
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    return X_train, X_test, y_train, y_test, feature_cols


def objective(trial, X_train, X_test, y_train, y_test):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
        "random_state": 42,
        "objective": "reg:squarederror",
        "n_jobs": -1,
    }

    model = XGBRegressor(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, preds)
    return float(rmse)


def main():
    settings.ensure_dirs()
    parquet_path = str(settings.gold_features_path)
    model_out = settings.artifacts_dir / "models" / "temperature_forecaster_tuned.joblib"
    report_out = settings.artifacts_dir / "reports" / "hyperparameter_search.json"
    X_train, X_test, y_train, y_test, feature_cols = prepare_data(parquet_path)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)
    with mlflow.start_run(run_name="xgboost_hyperparameter_search"):
        study = optuna.create_study(direction="minimize")
        study.optimize(
            lambda trial: objective(trial, X_train, X_test, y_train, y_test),
            n_trials=25,
        )

        best_params = study.best_params | {
            "random_state": 42,
            "objective": "reg:squarederror",
            "n_jobs": -1,
        }

        best_model = XGBRegressor(**best_params)
        best_model.fit(X_train, y_train)
        preds = best_model.predict(X_test)
        metrics = {
            "mae": float(mean_absolute_error(y_test, preds)),
            "rmse": float(root_mean_squared_error(y_test, preds)),
            "r2": float(r2_score(y_test, preds)),
        }

        model_package = {
            "model": best_model,
            "features": feature_cols,
            "best_params": best_params,
            "metrics": metrics,
        }

        Path(model_out).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model_package, model_out)
        payload = {
            "best_params": best_params,
            "metrics": metrics,
            "best_value": study.best_value,
            "n_trials": len(study.trials),
            "model_path": str(model_out),
        }

        report_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        mlflow.log_params(best_params)
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(str(report_out))
        mlflow.log_artifact(str(model_out))

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()