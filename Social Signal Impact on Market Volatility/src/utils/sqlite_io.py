from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd


def read_sqlite_table(db_path: Path, query: str, params: tuple | None = None) -> pd.DataFrame:
    conn = sqlite3.connect(str(db_path))
    try:
        return pd.read_sql_query(query, conn, params=params or ())
    finally:
        conn.close()
