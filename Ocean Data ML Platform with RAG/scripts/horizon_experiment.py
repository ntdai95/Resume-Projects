import json
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from xgboost import XGBRegressor
from app.core.settings import settings

HORIZONS_SAMPLES = [1, 30, 300, 900, 1800, 3600, 7200]
SAMPLE_INTERVAL_S = 1.015
MERGE_TOLERANCE = pd.Timedelta("2s")

XGB_PARAMS = dict(
    n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.9,
    colsample_bytree=0.9, random_state=42, objective="reg:squarederror", n_jobs=-1,
)

UNIVARIATE_FEATURES = ["lag_1", "lag_3", "lag_6", "trend", "hour", "dayofyear"]
CONTEXT_FEATURES = UNIVARIATE_FEATURES + ["salinity", "oxygen_corrected"]


def load_variable_series(df, source_variable, value_col):
    s = df[df["source_variable"] == source_variable][["time_ts", "normalized_value"]].copy()
    s = s.sort_values("time_ts").drop_duplicates(subset="time_ts")
    return s.rename(columns={"normalized_value": value_col})


def load_aligned_onc_series():
    df = pd.read_parquet(settings.silver_harmonized_path)
    df = df[df["dataset_id"] == "onc"].copy()
    df["time_ts"] = pd.to_datetime(df["time"])

    temp = load_variable_series(df, "Temperature", "temperature")
    salinity = load_variable_series(df, "salinity", "salinity")
    oxygen = load_variable_series(df, "oxygen_corrected", "oxygen_corrected")

    merged = pd.merge_asof(temp, salinity, on="time_ts", direction="backward", tolerance=MERGE_TOLERANCE)
    merged = pd.merge_asof(merged, oxygen, on="time_ts", direction="backward", tolerance=MERGE_TOLERANCE)
    merged = merged.dropna(subset=["salinity", "oxygen_corrected"]).reset_index(drop=True)

    merged["lag_1"] = merged["temperature"].shift(1)
    merged["lag_3"] = merged["temperature"].shift(3)
    merged["lag_6"] = merged["temperature"].shift(6)
    merged["trend"] = (merged["temperature"] - merged["lag_6"]) / 6
    merged["hour"] = merged["time_ts"].dt.hour
    merged["dayofyear"] = merged["time_ts"].dt.dayofyear
    return merged.dropna(subset=["lag_1", "lag_3", "lag_6"]).reset_index(drop=True)


def evaluate(y_test, preds):
    return {
        "rmse": float(root_mean_squared_error(y_test, preds)),
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
    }


def run_horizon(df, horizon):
    target = df["temperature"].shift(-horizon)
    valid = target.notna()
    X = df.loc[valid]
    y = target[valid]
    persistence_pred = df.loc[valid, "temperature"]

    split = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    persist_test = persistence_pred.iloc[split:]

    persist_metrics = evaluate(y_test, persist_test)

    uni_model = XGBRegressor(**XGB_PARAMS)
    uni_model.fit(X_train[UNIVARIATE_FEATURES], y_train)
    uni_metrics = evaluate(y_test, uni_model.predict(X_test[UNIVARIATE_FEATURES]))

    ctx_model = XGBRegressor(**XGB_PARAMS)
    ctx_model.fit(X_train[CONTEXT_FEATURES], y_train)
    ctx_metrics = evaluate(y_test, ctx_model.predict(X_test[CONTEXT_FEATURES]))

    return persist_metrics, uni_metrics, ctx_metrics, len(y_test)


def main():
    settings.ensure_dirs()
    df = load_aligned_onc_series()
    print(f"Aligned ONC series: {len(df)} rows spanning {df['time_ts'].min()} to {df['time_ts'].max()}")

    results = []
    for horizon in HORIZONS_SAMPLES:
        persist_metrics, uni_metrics, ctx_metrics, n_test = run_horizon(df, horizon)
        horizon_s = horizon * SAMPLE_INTERVAL_S
        results.append({
            "horizon_samples": horizon,
            "horizon_seconds": horizon_s,
            "test_rows": n_test,
            "persistence": persist_metrics,
            "xgboost_univariate": uni_metrics,
            "xgboost_with_context": ctx_metrics,
        })
        print(
            f"horizon={horizon} ({horizon_s:.0f}s)  "
            f"persistence_rmse={persist_metrics['rmse']:.5f}  "
            f"univariate_rmse={uni_metrics['rmse']:.5f}  "
            f"with_context_rmse={ctx_metrics['rmse']:.5f}"
        )

    settings.horizon_report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    horizons_s = [r["horizon_seconds"] for r in results]
    plt.figure()
    plt.plot(horizons_s, [r["persistence"]["rmse"] for r in results], marker="o", label="Naive persistence")
    plt.plot(horizons_s, [r["xgboost_univariate"]["rmse"] for r in results], marker="o", label="XGBoost (temperature only)")
    plt.plot(horizons_s, [r["xgboost_with_context"]["rmse"] for r in results], marker="o", label="XGBoost (+ salinity, oxygen)")
    plt.xscale("log")
    plt.xlabel("Forecast horizon (seconds, log scale)")
    plt.ylabel("RMSE (degC)")
    plt.title("Forecast error vs. horizon")
    plt.legend()
    plt.tight_layout()
    plt.savefig(settings.horizon_plot_path)
    plt.close()
    print("Saved horizon report and plot")


if __name__ == "__main__":
    main()
