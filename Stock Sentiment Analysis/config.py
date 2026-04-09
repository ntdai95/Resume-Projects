from pathlib import Path


TWEET_DB_PATH = Path("stock_influencer_tweets.db")
TRAIN_DB_PATH = Path("StocksTraining.db")
TEST_DB_PATH = Path("StocksTesting.db")

SENTIMENT_MODEL_NAME = "StephanAkkerman/FinTwitBERT-sentiment"
SENTIMENT_BATCH_SIZE = 32

PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

MAX_LAG = 5
SENTIMENT_LAGS = list(range(0, 6))