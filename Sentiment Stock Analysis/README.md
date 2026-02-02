# Sentiment Stock Analysis

An end-to-end quantitative data pipeline that integrates social media sentiment with financial time-series data to identify market signals. This system utilizes a hybrid database architecture (Neo4j + SQLite) and state-of-the-art NLP (FinBERT) to model the causal impact of social "chatter" on stock volatility.

## 🚀 System Architecture

- **Data Ingestion:** Automated scripts to fetch X (Twitter) streams and historical market data via `yfinance`.
- **Hybrid Storage:**
  - **Neo4j:** Graph database for mapping influencer-to-stock relationships and network centrality.
  - **SQLite:** Relational storage for high-frequency time-series returns and sentiment scores.
- **NLP Engine:** Utilizes **FinBERT** for high-precision financial sentiment classification.
- **Statistical Suite:** Built-in validation using Granger Causality, ADF tests, and GARCH(1,1) volatility modeling.
