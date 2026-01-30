from __future__ import annotations
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.config import get_paths


TARGET = "label_next_vol_5d"


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def save_fig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def eval_subset(df: pd.DataFrame, features: list[str], model) -> dict:
    for c in features:
        if c not in df.columns:
            df[c] = 0.0

    X = df[features]
    y = df[TARGET].values
    pred = model.predict(X)
    out = {
        "mae": float(mean_absolute_error(y, pred)),
        "rmse": rmse(y, pred),
        "n": int(len(df)),
    }

    if "vol_5d" in df.columns:
        true_dir = (df[TARGET].values > df["vol_5d"].values).astype(int)
        pred_dir = (pred > df["vol_5d"].values).astype(int)
        out["directional_accuracy"] = float((true_dir == pred_dir).mean())

    return out


def main() -> None:
    paths = get_paths()
    test = pd.read_parquet(paths.data_processed/"test_dataset.parquet")
    required = ["tweet_count","engagement_sum","unique_influencers","weighted_influence"]
    for c in required:
        if c not in test.columns:
            test[c] = 0.0

    if test.empty:
        print("Test dataset empty.")
        return

    model = joblib.load(paths.models/"model.pkl")
    schema = json.loads((paths.models/"feature_schema.json").read_text())
    full = schema["features"]
    test_market_only = test.copy()
    for c in ["tweet_count","engagement_sum","unique_influencers","weighted_influence"]:
        if c in test_market_only.columns:
            test_market_only[c] = 0.0

    test_market_plus_social = test.copy()
    if "weighted_influence" in test_market_plus_social.columns:
        test_market_plus_social["weighted_influence"] = 0.0

    results = {
        "market_only": eval_subset(test_market_only, full, model),
        "market_plus_social": eval_subset(test_market_plus_social, full, model),
        "market_plus_social_plus_graph": eval_subset(test, full, model),
    }

    (paths.data_reports/"metrics.json").write_text(json.dumps(results, indent=2))
    if "date" in test.columns:
        df = test.sort_values("date").copy()
        df["pred"] = model.predict(df[full])
        df["abs_err"] = np.abs(df[TARGET] - df["pred"])
        daily = df.groupby("date")["abs_err"].mean().reset_index()
        daily["roll7"] = daily["abs_err"].rolling(7).mean()
        plt.figure()
        plt.plot(daily["date"], daily["abs_err"], label="daily MAE")
        plt.plot(daily["date"], daily["roll7"], label="7d rolling")
        plt.legend()
        plt.title("Error over time (test)")
        save_fig(paths.figs/"error_over_time.png")

    if "ticker" in test.columns and "date" in test.columns:
        tkr = test["ticker"].mode().iloc[0]
        df = test[test["ticker"] == tkr].sort_values("date").copy()
        df["pred"] = model.predict(df[full])
        plt.figure()
        plt.plot(df["date"], df[TARGET], label="true")
        plt.plot(df["date"], df["pred"], label="pred")
        plt.legend()
        plt.title(f"Next-day rolling volatility (ticker={tkr})")
        save_fig(paths.figs/f"timeseries_{tkr}.png")

    print("Wrote metrics + figs to %s", paths.data_reports)


if __name__ == "__main__":
    main()
