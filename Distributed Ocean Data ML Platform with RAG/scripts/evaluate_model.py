import json
import matplotlib.pyplot as plt
import numpy as np
from app.core.settings import settings
from app.ml.experiment_tracker import log_run
from app.ml.train import train_xgboost_from_parquet


def main():
    settings.ensure_dirs()
    metrics, details = train_xgboost_from_parquet(str(settings.gold_features_path), str(settings.temp_model_path))
    settings.metrics_report_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("Saved metrics:")
    print(json.dumps(metrics, indent=2))
    if details and "y_test" in details and "preds" in details:
        y_test = np.array(details["y_test"])
        preds = np.array(details["preds"])
        plt.figure()
        plt.scatter(y_test, preds, alpha=0.5)
        plt.xlabel("Actual Temperature")
        plt.ylabel("Predicted Temperature")
        plt.title("Prediction vs Actual")
        plt.tight_layout()
        plt.savefig(settings.prediction_plot_path)
        plt.close()

        residuals = y_test - preds
        plt.figure()
        plt.hist(residuals, bins=30)
        plt.title("Residual Distribution")
        plt.xlabel("Prediction Error")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(settings.residual_plot_path)
        plt.close()
        print("Saved plots to artifacts/plots")
    else:
        print("Plot generation skipped (prediction details not returned)")

    log_run(
        run_name="evaluate_baseline_model",
        params={"model": "xgboost", "feature_count": len(details.get("feature_cols", []))},
        metrics=metrics,
    )


if __name__ == "__main__":
    main()