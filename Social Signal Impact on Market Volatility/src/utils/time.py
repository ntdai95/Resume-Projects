from __future__ import annotations
import pandas as pd


def to_utc_date(ts: pd.Series) -> pd.Series:
    t = pd.to_datetime(ts, utc=True, errors="coerce")
    return t.dt.date.astype("string")
