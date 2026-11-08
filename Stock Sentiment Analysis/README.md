# Stock Sentiment Analysis

This project asks whether what financial influencers post on X lines up with how
technology stocks move. It pairs tweet sentiment with daily price data, then tests the
relationship with correlation, Granger causality and GARCH models. The short answer is
that sentiment tracks same-day moves and says much more about volatility than it does
about tomorrow's return.

The stack is a hybrid database (SQLite and Neo4j), financial NLP with FinTwitBERT and econometric time-series analysis in `statsmodels` and `arch`.

---

## System overview

The pipeline runs in four stages:

1. Data collection
2. Hybrid data storage
3. Sentiment modeling
4. Statistical and volatility analysis

`main.py` runs all four in order, so the whole analysis reproduces from one command.

---

## Data collection

There are two data sources.

### Influencer tweets

Tweets come from the X (Twitter) API, from six accounts that move financial
conversation:

* Elon Musk
* Cathie Wood
* Ray Dalio
* Jim Cramer
* Michael Burry
* Donald Trump

Only the tweets that mention one of the tracked technology stocks are kept.

### Stock market data

Daily prices come from `yfinance` for ten technology companies:

* NVIDIA
* Apple
* Microsoft
* Alphabet
* Amazon
* Broadcom
* Meta Platforms
* TSMC
* Tesla
* Tencent

Each row carries OHLC, adjusted close and volume.

---

## Hybrid database architecture

The two stores answer different questions, so the project uses both.

### SQLite (relational storage)

SQLite holds the tables that get joined on a date:

* Tweet content and metadata
* Tweet-to-stock relationships
* Historical stock prices
* Daily sentiment signals

Time-series joins and daily aggregation are what relational storage is good at, so
everything the analysis reads lives here.

### Neo4j (graph database)

Neo4j holds the influencer relationships as a graph:

```
(Person) --POSTED--> (Tweet) --MENTIONS--> (Stock)
```

Walking that graph is how I look at which influencers talk about which stocks, and how
a single tweet propagates.

---

## Sentiment modeling

Sentiment comes from **FinTwitBERT**, a sentiment model trained on financial
Twitter-style text instead of general prose.

### Preprocessing

Each tweet is cleaned before it reaches the model:

* URLs and mentions are removed
* Text is normalized
* Non-English tweets are dropped

### Sentiment score

Every tweet gets one score from the model's two class probabilities:

```
sentiment = P(positive) - P(negative)
```

### Daily sentiment aggregation

Daily sentiment per stock is an engagement-weighted average, so a tweet that more
people actually saw counts for more:

```
weight = 1 + retweets + 0.5 * likes
```

---

## Statistical analysis pipeline

Four analyses run over the daily series.

### 1. Stationarity tests

Augmented Dickey-Fuller tests check that the series are suitable for the models that
follow.

### 2. Correlation analysis

This measures the same-day correlation between sentiment and price change, one stock at a time.

### 3. Granger causality tests

These test whether sentiment carries information about future price changes. Predictive
power is weak overall, and only a few cases reach statistical significance.

### 4. Volatility modeling (GARCH)

GARCH(1,1) models measure volatility persistence and how the market reacts to shocks.
Sentiment shows up more strongly in volatility than in return prediction.

---

## Outputs

Each run writes:

* Daily sentiment signals
* Sentiment against return plots
* Correlation statistics
* Granger causality results
* GARCH volatility parameters
* Final analysis tables

Everything is saved to disk, so a result can be traced back to the run that produced it.

---

## Tech stack

Python, SQLite, Neo4j, Hugging Face Transformers, PyTorch, statsmodels, arch, pandas,
matplotlib, yfinance, X API.

---

## Why I built it

Markets react to what gets said online, and I wanted to find out how much of that is
measurable and how much is only assumed. The point was never a trading system. It was to test
the statistical relationship between influencer sentiment and market behaviour, and to
report the result even where it came back weak.

---

## Repository structure

```
.
├── collect_x_stock_tweets.py
├── downloading_data_training.py
├── downloading_data_testing.py
├── sentiment_utils.py
├── stock_utils.py
├── analysis_utils.py
├── plotting_utils.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

`main.py` runs every stage in order.

---

## What I found

* Social sentiment correlates measurably with same-day stock movement.
* It predicts next-day returns poorly.
* It matters more for volatility dynamics than for the direction of a return.
* The effect is uneven across stocks, so no single influencer explains the market.

---

## Report and slides

The full methodology and results are written up here:

- [Project Report](report/Stock_Sentiment_Report.pdf)
- [Presentation Slides](report/Stock_Sentiment_Presentation.pdf)
