from __future__ import annotations
import pandas as pd
from src.config import get_paths


def _read(path):
    try:
        return pd.read_parquet(path)
    except Exception:
        return pd.DataFrame()


def main() -> None:
    paths = get_paths()
    events = _read(paths.data_processed/"events.parquet")
    prices = _read(paths.data_processed/"daily_features.parquet")
    labels = _read(paths.data_processed/"labels.parquet")
    graph = _read(paths.data_processed/"influencer_graph_features.parquet")
    if prices.empty or labels.empty:
        print("Missing price features/labels. Run: python -m src.features.price_features")
        return

    prices["date"] = pd.to_datetime(prices["date"])
    labels["date"] = pd.to_datetime(labels["date"])
    if events.empty:
        print("Events empty -> market-only ablation will dominate (expected if social DB has few links).")
        daily_social = pd.DataFrame(columns=["ticker","date","tweet_count","engagement_sum","unique_influencers","weighted_influence"])
    else:
        events["date"] = pd.to_datetime(events["event_date"])
        events["engagement"] = events[["like_count","retweet_count","reply_count","quote_count"]].sum(axis=1)
        if not graph.empty:
            g = graph[["influencer_username","influence_score"]]
            events = events.merge(g, on="influencer_username", how="left")
            events["influence_score"] = events["influence_score"].fillna(0.0)
        else:
            events["influence_score"] = 0.0

        daily_social = events.groupby(["stock_symbol","date"]).agg(
            tweet_count=("tweet_id","nunique"),
            engagement_sum=("engagement","sum"),
            unique_influencers=("influencer_username","nunique"),
            weighted_influence=("influence_score","sum"),
        ).reset_index().rename(columns={"stock_symbol":"ticker"})

    df = prices.merge(daily_social, on=["ticker","date"], how="left").merge(labels, on=["ticker","date"], how="left")
    for c in ["tweet_count","engagement_sum","unique_influencers","weighted_influence"]:
        if c not in df.columns:
            df[c] = 0.0
        else:
            df[c] = df[c].fillna(0.0)

    df = df.dropna(subset=["label_next_vol_5d"])
    df["year"] = df["date"].dt.year
    train = df[df["year"] == 2024].copy()
    test = df[df["year"] >= 2025].copy()
    train.to_parquet(paths.data_processed/"train_dataset.parquet", index=False)
    test.to_parquet(paths.data_processed/"test_dataset.parquet", index=False)
    print("Train rows=%d | Test rows=%d", len(train), len(test))


if __name__ == "__main__":
    main()
