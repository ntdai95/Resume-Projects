from __future__ import annotations
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingRegressor
from src.config import get_paths


TARGET = "label_next_vol_5d"


def main() -> None:
    paths = get_paths()
    train = pd.read_parquet(paths.data_processed/"train_dataset.parquet")
    required = ["tweet_count","engagement_sum","unique_influencers","weighted_influence"]
    for c in required:
        if c not in train.columns:
            train[c] = 0.0

    if train.empty:
        print("Training dataset empty. Check data/raw/ DBs and feature build steps.")
        return

    features = ["log_ret","vol_5d","vol_z20","volume","tweet_count","engagement_sum","unique_influencers","weighted_influence"]
    features = [c for c in features if c in train.columns]
    X = train[features]
    y = train[TARGET].astype(float)
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), features)
    ])

    model = HistGradientBoostingRegressor(max_depth=4, learning_rate=0.05, max_iter=400, random_state=42)
    pipe = Pipeline([("pre", pre), ("model", model)])
    pipe.fit(X, y)
    joblib.dump(pipe, paths.models/"model.pkl")
    (paths.models/"feature_schema.json").write_text(json.dumps({"target": TARGET, "features": features}, indent=2))
    print("Saved model -> %s", paths.models/"model.pkl")


if __name__ == "__main__":
    main()
