import sqlite3
from datetime import date
import pandas as pd
import yfinance as yf


TOP10_TECH = [
    ("NVDA",  "NVIDIA"),
    ("AAPL",  "Apple"),
    ("MSFT",  "Microsoft"),
    ("GOOG",  "Alphabet (Class C)"),
    ("AMZN",  "Amazon"),
    ("AVGO",  "Broadcom"),
    ("META",  "Meta Platforms"),
    ("TSM",   "Taiwan Semiconductor (TSMC)"),
    ("TSLA",  "Tesla"),
    ("TCEHY", "Tencent (ADR)"),
]

DB_PATH = "StocksTraining.db"
TABLE_COMPANIES = "companies"
TABLE_PRICES = "prices"
START = "2024-01-01"
END = "2024-12-31"


def ensure_schema(conn):
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_COMPANIES} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            name   TEXT NOT NULL
        );
    """)

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_PRICES} (
            ticker_id INTEGER NOT NULL,
            date      TEXT    NOT NULL,
            open      REAL,
            high      REAL,
            low       REAL,
            close     REAL,
            adj_close REAL,
            volume    INTEGER,
            PRIMARY KEY (ticker_id, date),
            FOREIGN KEY (ticker_id) REFERENCES {TABLE_COMPANIES}(id) ON DELETE CASCADE
        );
    """)

    conn.commit()


def upsert_companies(conn, tickers):
    cur = conn.cursor()
    for tkr, name in tickers:
        cur.execute(f"INSERT OR IGNORE INTO {TABLE_COMPANIES} (ticker, name) VALUES (?, ?);", (tkr, name))

    conn.commit()
    cur.execute(f"SELECT id, ticker FROM {TABLE_COMPANIES} WHERE ticker IN ({','.join('?'*len(tickers))});", [t for t, _ in tickers])
    mapping = {tkr: cid for cid, tkr in cur.fetchall()}
    return mapping


def fetch_prices(tickers, start, end):
    out = {}
    for t in tickers:
        df = yf.download(t, start=start, end=end, auto_adjust=False, progress=False)
        if df.empty:
            continue

        df = df.rename(columns={"Open": "open","High": "high","Low": "low", "Close": "close", "Adj Close": "adj_close", "Volume": "volume"})
        df.index = pd.to_datetime(df.index).date
        df.reset_index(names="date", inplace=True)
        out[t] = df[["date", "open", "high", "low", "close", "adj_close", "volume"]]
        
    return out


def insert_prices(conn, id_map, frames):
    cur = conn.cursor()
    for tkr, df in frames.items():
        ticker_id = id_map.get(tkr)
        if ticker_id is None:
            continue

        rows = [(ticker_id, d.isoformat() if isinstance(d, date) else str(d),
                 float(o) if pd.notna(o) else None,
                 float(h) if pd.notna(h) else None,
                 float(l) if pd.notna(l) else None,
                 float(c) if pd.notna(c) else None,
                 float(a) if pd.notna(a) else None,
                 int(v)   if pd.notna(v) else None)
                 for d,o,h,l,c,a,v in df.itertuples(index=False, name=None)
               ]
        
        cur.executemany(
            f"""INSERT OR REPLACE INTO {TABLE_PRICES}
                (ticker_id, date, open, high, low, close, adj_close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
            rows
        )
        
    conn.commit()


def main():
    tickers_only = [t for t, _ in TOP10_TECH]
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_schema(conn)
        id_map = upsert_companies(conn, TOP10_TECH)
        frames = fetch_prices(tickers_only, START, END)
        insert_prices(conn, id_map, frames)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
