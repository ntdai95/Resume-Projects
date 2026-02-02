from statsmodels.tsa.stattools import grangercausalitytests
from arch import arch_model


def run_stats(ticker, df):
    if len(df) <= 10: 
        print(f"Skipping {ticker}: Not enough data (only {len(df)} rows).")
        return None

    try:
        gc = grangercausalitytests(df[["oneDayChange", "sentiment"]], maxlag=5, verbose=False)
        p_val = min([gc[i][0]['ssr_chi2test'][1] for i in range(1, 6)])
    except ValueError:
        return None
    
    try:
        am = arch_model(df["oneDayChange"] * 100, vol="Garch", p=1, q=1)
        res = am.fit(disp="off")
        g_beta = res.params['beta[1]']
    except:
        g_beta = 0
    
    return {"ticker": ticker, "granger_p": p_val, "garch_beta": g_beta}