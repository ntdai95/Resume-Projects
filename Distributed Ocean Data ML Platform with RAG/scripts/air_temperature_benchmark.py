import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from xgboost import XGBRegressor
from app.core.settings import settings

ERDDAP_URL = (
    "https://dap.oceannetworks.ca/erddap/tabledap/scalar_1203278.csv"
    "?time,air_temperature,WindSpeed,pressure1,humidity,direction1"
)
RAW_CSV_PATH = settings.data_dir / "raw" / "onc_met" / "baynes_sound_met.csv"
HORIZONS_MINUTES = [1, 15, 60, 180, 360, 720, 1440]


def ensure_raw_csv():
    if RAW_CSV_PATH.exists():
        return
    RAW_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(ERDDAP_URL, timeout=120)
    response.raise_for_status()
    RAW_CSV_PATH.write_bytes(response.content)

XGB_PARAMS = dict(
    n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.9,
    colsample_bytree=0.9, random_state=42, objective="reg:squarederror", n_jobs=-1,
)

UNIVARIATE_FEATURES = ["lag_1", "lag_3", "lag_6", "trend", "hour", "dayofyear"]
CONTEXT_FEATURES = UNIVARIATE_FEATURES + ["pressure1", "WindSpeed"]


def load_series():
    ensure_raw_csv()
    df = pd.read_csv(RAW_CSV_PATH, skiprows=[1])
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").drop_duplicates(subset="time").reset_index(drop=True)
    df["lag_1"] = df["air_temperature"].shift(1)
    df["lag_3"] = df["air_temperature"].shift(3)
    df["lag_6"] = df["air_temperature"].shift(6)
    df["trend"] = (df["air_temperature"] - df["lag_6"]) / 6
    df["hour"] = df["time"].dt.hour
    df["dayofyear"] = df["time"].dt.dayofyear
    return df.dropna(subset=["lag_1", "lag_3", "lag_6"]).reset_index(drop=True)


def evaluate(y_test, preds):
    return {
        "rmse": float(root_mean_squared_error(y_test, preds)),
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
    }


def run_horizon(df, horizon):
    target = df["air_temperature"].shift(-horizon)
    valid = target.notna()
    X = df.loc[valid]
    y = target[valid]
    persistence_pred = df.loc[valid, "air_temperature"]

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
    df = load_series()
    print(f"Rows: {len(df)}, spanning {df['time'].min()} to {df['time'].max()}")

    results = []
    for horizon in HORIZONS_MINUTES:
        persist_metrics, uni_metrics, ctx_metrics, n_test = run_horizon(df, horizon)
        results.append({
            "horizon_minutes": horizon,
            "test_rows": n_test,
            "persistence": persist_metrics,
            "xgboost_univariate": uni_metrics,
            "xgboost_with_context": ctx_metrics,
        })
        print(
            f"horizon={horizon}min  "
            f"persistence_rmse={persist_metrics['rmse']:.4f}  "
            f"univariate_rmse={uni_metrics['rmse']:.4f}  "
            f"with_context_rmse={ctx_metrics['rmse']:.4f}"
        )

    settings.air_temp_report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    horizons = [r["horizon_minutes"] for r in results]
    plt.figure()
    plt.plot(horizons, [r["persistence"]["rmse"] for r in results], marker="o", label="Naive persistence")
    plt.plot(horizons, [r["xgboost_univariate"]["rmse"] for r in results], marker="o", label="XGBoost (air temp only)")
    plt.plot(horizons, [r["xgboost_with_context"]["rmse"] for r in results], marker="o", label="XGBoost (+ pressure, wind)")
    plt.xscale("log")
    plt.xlabel("Forecast horizon (minutes, log scale)")
    plt.ylabel("RMSE (degC)")
    plt.title("Air temperature forecast error vs. horizon")
    plt.legend()
    plt.tight_layout()
    plt.savefig(settings.air_temp_plot_path)
    plt.close()
    print("Saved air temperature benchmark report and plot")


if __name__ == "__main__":
    main()
