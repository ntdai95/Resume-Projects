import matplotlib.pyplot as plt
from config import PLOTS_DIR


def plot_analysis(df, ticker):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df.index, df['oneDayChange'], color='tab:blue', label='Return')
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['sentiment'], color='tab:red', alpha=0.6, label='Sentiment')
    plt.title(f"Ticker: {ticker} - Sentiment vs returns")
    plt.savefig(PLOTS_DIR / f"{ticker}_plot.png")
    plt.close()