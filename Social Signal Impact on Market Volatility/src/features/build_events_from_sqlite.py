from __future__ import annotations
import pandas as pd
from src.config import get_paths
from src.utils.sqlite_io import read_sqlite_table
from src.utils.time import to_utc_date


def main() -> None:
    paths = get_paths()
    db = paths.data_raw / "stock_influencer_tweets.db"
    out_path = paths.data_processed / "events.parquet"
    if not db.exists():
        print("Missing %s. This offline zip should include it in data/raw/.", db)
        pd.DataFrame().to_parquet(out_path, index=False)
        return

    tweets = read_sqlite_table(db, "SELECT * FROM tweets")
    users = read_sqlite_table(db, "SELECT * FROM users")
    ts = read_sqlite_table(db, "SELECT * FROM tweet_stocks")
    if tweets.empty or ts.empty:
        print("Tweets or tweet_stocks is empty. Writing empty events.")
        pd.DataFrame().to_parquet(out_path, index=False)
        return

    df = ts.merge(tweets, left_on="tweet_id", right_on="id", how="left", suffixes=("", "_tweet"))
    df = df.merge(users, left_on="user_id", right_on="id", how="left", suffixes=("", "_user"))
    out = pd.DataFrame({
        "tweet_id": df["tweet_id"],
        "stock_symbol": df["stock_symbol"],
        "influencer_id": df["user_id"],
        "influencer_username": df["username"],
        "influencer_name": df["name"],
        "created_at": df["created_at"],
        "event_date": to_utc_date(df["created_at"]),
        "like_count": df["like_count"].fillna(0).astype(int),
        "retweet_count": df["retweet_count"].fillna(0).astype(int),
        "reply_count": df["reply_count"].fillna(0).astype(int),
        "quote_count": df["quote_count"].fillna(0).astype(int),
        "lang": df["lang"],
        "text": df["text"],
    }).dropna(subset=["event_date","stock_symbol","influencer_username"])

    out.to_parquet(out_path, index=False)
    print("Wrote %d rows -> %s", len(out), out_path)


if __name__ == "__main__":
    main()
