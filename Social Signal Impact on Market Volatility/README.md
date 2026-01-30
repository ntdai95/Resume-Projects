# Social Signal Impact on Market Volatility

This project studies whether **social media activity from influential accounts provides incremental signal for short-horizon equity volatility prediction**, beyond traditional price-based features.

The emphasis is on **rigorous data science practice**:

- strict temporal splits
- reproducible, offline pipelines
- feature ablations
- robustness to missing data

The project is intentionally **model-simple and evaluation-heavy**, reflecting how new-grad Data Science roles at Big Tech are assessed.

---

### Step 1: Build Social Event Features (SQLite)

Aggregate tweet counts and engagement by stock and day.

python -m src.features.build_events_from_sqlite

Creates:

- data/processed/events.parquet

---

### Step 2: Build Market Features and Labels (SQLite)

Generate log returns, rolling volatility, volume statistics, and next-day labels.

python -m src.features.price_features

Creates:

- data/processed/daily_features.parquet
- data/processed/labels.parquet

---

### Step 3: (Optional) Build Graph Features (Neo4j)

Extract influencer-level graph features if Neo4j is running and populated.

python -m src.features.graph_features

Creates (optional):

- data/processed/influencer_graph_features.parquet

If Neo4j is unavailable, this step can be skipped safely.

---

### Step 4: Build Final Train/Test Datasets

Merge all features and enforce strict temporal separation.

python -m src.features.build_dataset

Creates:

- data/processed/train_dataset.parquet
- data/processed/test_dataset.parquet

---

### Step 5: Train the Model

Train a regression model using a fixed, schema-stable feature set.

python -m src.modeling.train

Creates:

- models/model.pkl
- models/feature_schema.json

---

### Step 6: Evaluate and Run Feature Ablations

Evaluate performance on the test set and compute ablations:

- market-only
- market + social
- market + social + graph

python -m src.modeling.evaluate

Creates:

- data/reports/metrics.json
- data/reports/figs/error_over_time.png
- data/reports/figs/timeseries_`<TICKER>`.png
