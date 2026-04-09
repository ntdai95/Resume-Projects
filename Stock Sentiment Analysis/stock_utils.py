import pandas as pd


def build_merged_data(daily_sent, all_prices, ticker, lags):
    stock_df = all_prices[all_prices['ticker'] == ticker].copy()
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df = stock_df.sort_values('date').set_index('date')
    stock_df['oneDayChange'] = stock_df['close'].pct_change()
    
    sent_df = daily_sent[daily_sent['stock'] == ticker].copy()
    sent_df['date'] = pd.to_datetime(sent_df['date'])
    sent_df = sent_df.set_index('date')
    
    merged = stock_df.join(sent_df['sentiment'], how='inner')
    for lag in lags:
        merged[f'sent_lag_{lag}'] = merged['sentiment'].shift(lag)
    
    return merged.dropna()