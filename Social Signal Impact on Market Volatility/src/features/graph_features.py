from __future__ import annotations
import pandas as pd
import numpy as np
from neo4j import GraphDatabase
from src.config import get_paths, get_neo4j_config


CYPHER = """
MATCH (u:Person)-[:POSTED]->(t:Tweet)
OPTIONAL MATCH (t)-[:MENTIONS]->(s:Stock)
WITH u,
     count(DISTINCT t) AS tweet_count,
     count(DISTINCT s) AS distinct_stocks,
     sum(coalesce(t.like_count,0)) AS total_likes,
     sum(coalesce(t.retweet_count,0)) AS total_retweets,
     sum(coalesce(t.reply_count,0)) AS total_replies,
     sum(coalesce(t.quote_count,0)) AS total_quotes
RETURN u.id AS influencer_id,
       u.username AS influencer_username,
       u.name AS influencer_name,
       tweet_count,
       distinct_stocks,
       total_likes, total_retweets, total_replies, total_quotes
"""


def main() -> None:
    paths = get_paths()
    neo = get_neo4j_config()
    out_path = paths.data_processed / "influencer_graph_features.parquet"
    try:
        driver = GraphDatabase.driver(neo.uri, auth=(neo.user, neo.password))
        with driver.session(database=neo.database) as s:
            rows = [dict(r) for r in s.run(CYPHER)]

        driver.close()
    except Exception as e:
        print("Neo4j unavailable or query failed (%s). Writing empty graph features.", e)
        pd.DataFrame().to_parquet(out_path, index=False)
        return

    df = pd.DataFrame(rows)
    if df.empty:
        pd.DataFrame().to_parquet(out_path, index=False)
        return

    df["engagement_total"] = df[["total_likes","total_retweets","total_replies","total_quotes"]].sum(axis=1)
    df["influence_score"] = np.log1p(df["engagement_total"].astype(float) + 1.0)
    df.to_parquet(out_path, index=False)
    print("Wrote %s", out_path)


if __name__ == "__main__":
    main()
