import pandas as pd
from app.ml.train import train_xgboost_from_parquet


def test_train(tmp_path):
    df = pd.DataFrame({
        "hour": list(range(1,11)),
        "dayofyear": [1] * 10,
        "month": [1] * 10,
        "lag_1": list(range(1,11)),
        "lag_3": list(range(1,11)),
        "lag_6": list(range(1,11)),
        "normalized_value": list(range(1,11)),
        "source_variable": ["temp"] * 10,
        "canonical_variable": ["sea_water_temperature"] * 10,
        "units": ["K"] * 10,
        "normalized_unit": ["degC"] * 10,
        "source_file": ["a"] * 10,
        "dataset_id": ["onc"] * 10,
        "provenance_transform": ["x"] * 10,
        "time_ts": ["2024-01-01"] * 10,
    })

    p = tmp_path/"f.parquet"
    df.to_parquet(p)
    metrics, details = train_xgboost_from_parquet(p, tmp_path/"m.joblib")
    assert "mae" in metrics
    assert "feature_importance" in details