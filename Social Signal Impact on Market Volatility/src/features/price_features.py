from __future__ import annotations
import pandas as pd
import numpy as np
from src.config import get_paths
from src.utils.sqlite_io import read_sqlite_table


def _load_prices(db_path):
    q = """
    SELECT c.ticker, p.date, p.open, p.high, p.low, p.close, p.adj_close, p.volume
    FROM prices p
    JOIN companies c ON c.id = p.ticker_id
    """
    df = read_sqlite_table(db_path, q)
    if df.empty:
        return df
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values(["ticker","date"])
    return df


def _add_features(px: pd.DataFrame) -> pd.DataFrame:
    px = px.copy()
    px["price"] = px["adj_close"].where(px["adj_close"].notna(), px["close"])
    px["log_ret"] = px.groupby("ticker")["price"].transform(lambda s: np.log(s).diff())
    px["vol_5d"] = px.groupby("ticker")["log_ret"].transform(lambda s: s.rolling(5).std())
    roll_mean = px.groupby("ticker")["volume"].rolling(20).mean().reset_index(level=0, drop=True)
    roll_std = px.groupby("ticker")["volume"].rolling(20).std().reset_index(level=0, drop=True).replace(0, np.nan)
    px["vol_z20"] = (px["volume"] - roll_mean) / roll_std
    px["label_next_vol_5d"] = px.groupby("ticker")["vol_5d"].shift(-1)
    px["label_next_vol_z20"] = px.groupby("ticker")["vol_z20"].shift(-1)
    return px


def main() -> None:
    paths = get_paths()
    train_db = paths.data_raw / "StocksTraining.db"
    test_db = paths.data_raw / "StocksTesting.db"
    if not train_db.exists() or not test_db.exists():
        print("Missing price DBs in data/raw/.")
        return

    train = _load_prices(train_db)
    test = _load_prices(test_db)
    allp = pd.concat([train, test], ignore_index=True)
    if allp.empty:
        print("No price rows found.")
        return

    allp = _add_features(allp)
    feats = allp[["ticker","date","log_ret","vol_5d","vol_z20","volume"]].copy()
    labels = allp[["ticker","date","label_next_vol_5d","label_next_vol_z20"]].copy()
    feats.to_parquet(paths.data_processed/"daily_features.parquet", index=False)
    labels.to_parquet(paths.data_processed/"labels.parquet", index=False)
    print("Wrote daily_features.parquet + labels.parquet")


if __name__ == "__main__":
    main()
