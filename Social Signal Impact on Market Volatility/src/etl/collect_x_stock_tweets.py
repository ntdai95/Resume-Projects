import os
import time
import sqlite3
import requests
from neo4j import GraphDatabase
from dotenv import load_dotenv


load_dotenv()

# Store the X Bearer Token in the .env file for security
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
X_API_BASE_URL = "https://api.x.com/2"
INFLUENCERS = [
    "elonmusk",
    "realDonaldTrump",
    "CathieDWood",
    "jimcramer",
    "michaeljburry",
    "RayDalio",
]

START_TIME = "2024-01-01T00:00:00Z"
END_TIME   = "2025-12-31T23:59:59Z"
MAX_PAGES_PER_USER = 10
SQLITE_DB_PATH = "stock_influencer_tweets.db"
NEO4J_URI      = "bolt://localhost:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "neo4jproject"
STOCKS = [
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

STOCK_KEYWORDS = {symbol: {symbol.lower(), company.lower()} for symbol, company in STOCKS}
def x_headers():
    if not X_BEARER_TOKEN:
        raise RuntimeError("Missing X_BEARER_TOKEN. Set it in the .env file.")
    
    return {"Authorization": f"Bearer {X_BEARER_TOKEN}"}


def get_user_by_username(username):
    url = f"{X_API_BASE_URL}/users/by/username/{username}"
    params = {"user.fields": "name,username,created_at,public_metrics"}

    resp = requests.get(url, headers=x_headers(), params=params)
    if resp.status_code == 200:
        return resp.json().get("data")
    
    print(f"[WARN] Could not fetch @{username}: {resp.text}")
    return None


def get_user_tweets(user_id):
    url = f"{X_API_BASE_URL}/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "start_time": START_TIME,
        "end_time": END_TIME,
        "tweet.fields": "created_at,public_metrics,lang,entities",
    }

    all_tweets = []
    next_token = None
    for _ in range(MAX_PAGES_PER_USER):
        if next_token:
            params["pagination_token"] = next_token

        resp = requests.get(url, headers=x_headers(), params=params)
        if resp.status_code != 200:
            print("[WARN] Tweet fetch failed:", resp.text)
            break

        data = resp.json()
        tweets = data.get("data", [])
        all_tweets.extend(tweets)
        next_token = data.get("meta", {}).get("next_token")
        if not next_token:
            break

        time.sleep(1)

    print("[INFO] Next Token:", next_token)
    return all_tweets


def extract_stocks_from_text(text):
    text_lower = text.lower()
    matches = []
    for symbol, keywords in STOCK_KEYWORDS.items():
        if any(k in text_lower for k in keywords):
            matches.append(symbol)

    return matches


def init_sqlite():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            text TEXT,
            created_at TEXT,
            like_count INTEGER,
            retweet_count INTEGER,
            reply_count INTEGER,
            quote_count INTEGER,
            lang TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tweet_stocks (
            tweet_id TEXT,
            stock_symbol TEXT,
            PRIMARY KEY (tweet_id, stock_symbol)
        )
    """)

    cur.executemany(
        "INSERT OR IGNORE INTO stocks(symbol, name) VALUES (?, ?)",
        STOCKS
    )

    conn.commit()
    return conn


def insert_user(conn, user):
    conn.execute(
        "INSERT OR REPLACE INTO users(id, username, name) VALUES (?, ?, ?)",
        (user["id"], user["username"], user["name"])
    )

    conn.commit()


def insert_tweet(conn, tweet, user_id, stocks):
    metrics = tweet.get("public_metrics", {})
    conn.execute("""
        INSERT OR REPLACE INTO tweets(
            id, user_id, text, created_at,
            like_count, retweet_count, reply_count, quote_count, lang
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tweet["id"], user_id, tweet["text"], tweet["created_at"],
        metrics.get("like_count", 0),
        metrics.get("retweet_count", 0),
        metrics.get("reply_count", 0),
        metrics.get("quote_count", 0),
        tweet.get("lang")
    ))

    for s in stocks:
        conn.execute(
            "INSERT OR IGNORE INTO tweet_stocks(tweet_id, stock_symbol) VALUES (?, ?)",
            (tweet["id"], s)
        )

    conn.commit()


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )


    def close(self):
        self.driver.close()


    def init_constraints(self):
        with self.driver.session(database="stock-influencer-tweets-neo4j") as s:
            s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE")
            s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tweet) REQUIRE t.id IS UNIQUE")
            s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Stock) REQUIRE s.symbol IS UNIQUE")


    def insert_stock_relations(self, tweet, user_id, user_username, user_name, stocks):
        metrics = tweet.get("public_metrics", {})
        with self.driver.session(database="stock-influencer-tweets-neo4j") as s:
            s.run("""
            MERGE (u:Person {id: $uid})
              ON CREATE SET u.username = $uname,
                            u.name     = $name
              ON MATCH  SET u.username = $uname,
                            u.name     = $name

            MERGE (t:Tweet {id: $tid})
              ON CREATE SET t.text          = $text,
                            t.created_at    = $ca,
                            t.like_count    = $lc,
                            t.retweet_count = $rc,
                            t.reply_count   = $rp,
                            t.quote_count   = $qc,
                            t.lang          = $lang

            MERGE (u)-[:POSTED]->(t)
            WITH t
            UNWIND $stocks AS sym
                MERGE (st:Stock {symbol: sym})
                MERGE (t)-[:MENTIONS]->(st)
            """, {
                "uid":   user_id,
                "uname": user_username,
                "name":  user_name,
                "tid":   tweet["id"],
                "text":  tweet["text"],
                "ca":    tweet["created_at"],
                "lc":    metrics.get("like_count", 0),
                "rc":    metrics.get("retweet_count", 0),
                "rp":    metrics.get("reply_count", 0),
                "qc":    metrics.get("quote_count", 0),
                "lang":  tweet.get("lang"),
                "stocks": stocks
            })


def main():
    conn = init_sqlite()
    neo = Neo4jClient()
    neo.init_constraints()
    for username in INFLUENCERS:
        print(f"\n[INFO] Fetching @{username}")
        user = get_user_by_username(username)
        if not user:
            continue

        insert_user(conn, user)
        tweets = get_user_tweets(user["id"])
        print(f"[INFO] Total tweets fetched: {len(tweets)}")
        for tweet in tweets:
            stocks = extract_stocks_from_text(tweet.get("text", ""))
            if not stocks:
                continue

            insert_tweet(conn, tweet, user["id"], stocks)
            neo.insert_stock_relations(tweet, user["id"], user["username"], user["name"], stocks)

        print(f"[INFO] Done with @{username}")

    neo.close()
    conn.close()
    print("\n[INFO] All finished.")


if __name__ == "__main__":
    main()
