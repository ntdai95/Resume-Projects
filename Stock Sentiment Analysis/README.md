# Stock Sentiment Analysis

An end-to-end quantitative data pipeline that integrates social media sentiment with financial time-series data to evaluate whether influencer-driven online discussions are associated with stock returns and market volatility.

The system combines a hybrid database architecture (Neo4j + SQLite), financial NLP (FinTwitBERT), and econometric time-series analysis (correlation, Granger causality, and GARCH modeling) to study relationships between social sentiment and stock market behavior.

---

## 🚀 System Overview

The pipeline consists of four stages:

1. **Data Collection**
2. **Hybrid Data Storage**
3. **Sentiment Modeling**
4. **Statistical & Volatility Analysis**

The entire workflow is reproducible and fully automated via Python scripts.

---

## 📡 Data Collection

Two primary data sources are used:

### Influencer Tweets

Tweets are collected using the X (Twitter) API from major financial influencers, including:

* Elon Musk
* Cathie Wood
* Ray Dalio
* Jim Cramer
* Michael Burry
* Donald Trump

Tweets mentioning major technology stocks are retained and stored.

### Stock Market Data

Historical daily stock prices are downloaded using `yfinance` for major technology companies, including:

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

Price data include OHLC, adjusted close, and volume.

---

## 🗄 Hybrid Database Architecture

The system uses two complementary storage systems:

### SQLite (Relational Storage)

Used for:

* Tweet content and metadata
* Tweet–stock relationships
* Historical stock prices
* Daily sentiment signals

Relational storage enables efficient time-series joins and aggregation.

### Neo4j (Graph Database)

Used to model influencer relationships:

<pre class="overflow-visible! px-0!" data-start="2124" data-end="2182"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>(Person) </span><span>--POSTED--</span><span>> (Tweet) </span><span>--MENTIONS--</span><span>> (Stock)
</span></span></code></div></div></pre>

This allows exploration of influencer–stock networks and tweet propagation patterns.

---

## 🧠 Sentiment Modeling

Tweet sentiment is computed using  **FinTwitBERT** , a financial sentiment model designed for Twitter-style financial text.

### Preprocessing

Tweets are cleaned by:

* Removing URLs and mentions
* Normalizing text
* Filtering to English tweets

### Sentiment Score

Each tweet receives a sentiment score:

<pre class="overflow-visible! px-0!" data-start="2604" data-end="2649"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>sentiment</span><span> = P(positive) − P(negative)
</span></span></code></div></div></pre>

### Daily Sentiment Aggregation

Daily sentiment per stock is computed using engagement-weighted averaging:

<pre class="overflow-visible! px-0!" data-start="2759" data-end="2802"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>weight</span><span> = </span><span>1</span><span> + retweets + </span><span>0.5</span><span> × likes
</span></span></code></div></div></pre>

This emphasizes tweets with higher market visibility.

---

## 📊 Statistical Analysis Pipeline

The following analyses are performed:

### 1. Stationarity Tests

Augmented Dickey-Fuller tests verify time-series suitability for modeling.

### 2. Correlation Analysis

Same-day correlation between sentiment and price changes is measured across stocks.

### 3. Granger Causality Tests

Tests whether sentiment signals provide predictive information for future price changes.

Results show weak predictive power overall, with limited cases of statistical significance.

### 4. Volatility Modeling (GARCH)

GARCH(1,1) models are used to examine volatility persistence and market reactions to shocks.

Results suggest sentiment contributes more strongly to volatility dynamics than to return prediction.

---

## 📈 Outputs

The pipeline generates:

* Daily sentiment signals
* Sentiment vs. return plots
* Correlation statistics
* Granger causality results
* GARCH volatility parameters
* Final analysis tables

Results are saved automatically for reproducibility.

---

## 🛠 Tech Stack

Core technologies used:

* Python
* SQLite
* Neo4j
* Hugging Face Transformers
* PyTorch
* statsmodels
* arch
* pandas
* matplotlib
* yfinance
* X API

---

## 🎯 Project Motivation

Financial markets increasingly react to online discourse. This project explores whether large-scale influencer sentiment carries measurable signals related to stock market movements and volatility.

The goal is not to build a trading system, but to evaluate the statistical relationships between social sentiment and market behavior.

---

## 📂 Repository Structure

<pre class="overflow-visible! px-0!" data-start="4437" data-end="4688"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>.
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
</span></span></code></div></div></pre>

Running `main.py` executes the end-to-end analysis pipeline.

---

## 📌 Key Takeaways

* Social sentiment shows measurable correlation with same-day stock movements.
* Predictive power for next-day returns is limited.
* Sentiment appears more relevant to volatility dynamics than return direction.
* Influencer-driven discussion impacts stocks unevenly.

---

## 📄 Project Report & Slides

Full methodology and results are documented here:

- 📘 [Project Report](report/Stock Sentiment Report.pdf)
- 📊 [Presentation Slides](report/Stock Sentiment Presentation.pdf)
