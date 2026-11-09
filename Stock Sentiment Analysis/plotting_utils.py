import matplotlib.pyplot as plt
import pandas as pd
from config import PLOTS_DIR


def plot_analysis(df, ticker):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df.index, df['oneDayChange'], color='tab:blue', label='Return')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Daily return', color='tab:blue')
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['sentiment'], color='tab:red', alpha=0.6, label='Sentiment')
    ax2.set_ylabel('Sentiment score', color='tab:red')
    plt.title(f"Ticker: {ticker} - Sentiment vs returns")
    fig.tight_layout()
    plt.savefig(PLOTS_DIR / f"{ticker}_plot.png")
    plt.close()


def plot_summary(results):
    if not results:
        return

    frame = pd.DataFrame(results).sort_values('ticker')
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    axes[0].bar(frame['ticker'], frame['corr_lag0'], color='tab:blue')
    axes[0].set_title('Same-day sentiment-return correlation')

    axes[1].bar(frame['ticker'], frame['granger_p'], color='tab:red')
    axes[1].axhline(0.05, color='black', linestyle='--', linewidth=1)
    axes[1].set_title('Minimum Granger p-value across lags 1-5')

    axes[2].bar(frame['ticker'], frame['garch_beta'], color='tab:green')
    axes[2].set_title('GARCH(1,1) volatility persistence')
    axes[2].set_xlabel('Ticker')

    for axis in axes:
        axis.grid(axis='y', alpha=0.25)

    fig.tight_layout()
    fig.savefig(PLOTS_DIR / 'results_summary.png')
    plt.close(fig)
