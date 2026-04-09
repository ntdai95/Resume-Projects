import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from arch import arch_model


def run_stats(ticker, df):
    if len(df) <= 10:
        print(f"Skipping {ticker}: Not enough data (only {len(df)} rows).")
        return None

    try:
        adf_ret_p = adfuller(df["oneDayChange"].dropna())[1]
    except Exception:
        adf_ret_p = np.nan

    try:
        adf_sent_p = adfuller(df["sentiment"].dropna())[1]
    except Exception:
        adf_sent_p = np.nan

    try:
        corr_lag0 = df[["oneDayChange", "sentiment"]].corr(method="pearson").iloc[0, 1]
    except Exception:
        corr_lag0 = np.nan

    try:
        gc_df = df[["oneDayChange", "sentiment"]].dropna()
        gc = grangercausalitytests(gc_df, maxlag=5, verbose=False)
        p_val = min([gc[i][0]["ssr_chi2test"][1] for i in range(1, 6)])
    except ValueError:
        return None
    except Exception:
        p_val = np.nan

    try:
        am = arch_model(df["oneDayChange"].dropna() * 100, vol="Garch", p=1, q=1)
        res = am.fit(disp="off")
        g_beta = float(res.params.get("beta[1]", np.nan))
    except Exception:
        g_beta = np.nan

    return {
        "ticker": ticker,
        "corr_lag0": corr_lag0,
        "adf_ret_p": adf_ret_p,
        "adf_sent_p": adf_sent_p,
        "granger_p": p_val,
        "garch_beta": g_beta,
    }