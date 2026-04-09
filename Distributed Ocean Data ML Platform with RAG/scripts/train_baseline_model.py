import json
from app.core.settings import settings
from app.ml.train import train_xgboost_from_parquet


def main():
    settings.ensure_dirs()
    metrics, details = train_xgboost_from_parquet(str(settings.gold_features_path), str(settings.model_path))
    print(json.dumps(
        {
            "message": "Baseline model trained successfully",
            "metrics": metrics,
            "num_features": len(details["feature_cols"]),
            "model_path": str(settings.model_path),
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()