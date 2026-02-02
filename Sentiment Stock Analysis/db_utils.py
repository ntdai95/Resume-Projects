import sqlite3
import pandas as pd


def get_companies_list(tweet_conn):
    return pd.read_sql_query("SELECT symbol FROM stocks", tweet_conn)["symbol"].unique().tolist()


def load_all_prices(train_path, test_path):
    """Merges prices from both generated databases."""
    with sqlite3.connect(train_path) as conn_train, sqlite3.connect(test_path) as conn_test:
        query = """
            SELECT c.ticker, p.date, p.close 
            FROM prices p 
            JOIN companies c ON p.ticker_id = c.id
        """
        
        df_train = pd.read_sql_query(query, conn_train)
        df_test = pd.read_sql_query(query, conn_test)

    return pd.concat([df_train, df_test]).drop_duplicates()