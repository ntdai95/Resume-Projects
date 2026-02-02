import sqlite3
import pandas as pd
import os
from config import TWEET_DB_PATH, TRAIN_DB_PATH, TEST_DB_PATH, SENTIMENT_LAGS
import db_utils, sentiment_utils, stock_utils, analysis_utils, plotting_utils


def main():
    RESULT_DIR = "result"
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)

    with sqlite3.connect(TWEET_DB_PATH) as t_conn:
        tokenizer, model = sentiment_utils.load_finbert()
        daily_sent = sentiment_utils.compute_daily_average_sentiment(t_conn, tokenizer, model)
        all_prices = db_utils.load_all_prices(TRAIN_DB_PATH, TEST_DB_PATH)
        tickers = db_utils.get_companies_list(t_conn)    
        final_results = []
        for ticker in tickers:
            merged = stock_utils.build_merged_data(daily_sent, all_prices, ticker, SENTIMENT_LAGS)
            if not merged.empty:
                stats = analysis_utils.run_stats(ticker, merged)
                if stats:
                    final_results.append(stats)
                    plotting_utils.plot_analysis(merged, ticker)
        
        output_path = os.path.join(RESULT_DIR, "final_analysis.csv")
        pd.DataFrame(final_results).to_csv(output_path, index=False)


if __name__ == "__main__":
    main()