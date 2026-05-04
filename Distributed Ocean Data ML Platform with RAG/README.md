# 🌊 Ocean Data Harmonization + Distributed ML + RAG System

A **production-style machine learning platform** that ingests heterogeneous ocean datasets, harmonizes them using Apache Spark, trains forecasting models, and exposes a Retrieval-Augmented Generation (RAG) interface for natural-language exploration of ocean data.

This project demonstrates a full  **end-to-end ML system** , including:

* distributed data processing with Apache Spark
* NetCDF dataset ingestion and metadata extraction
* SHA256 source manifest generation
* Bronze → Silver → Gold data pipeline
* data harmonization and feature engineering
* XGBoost forecasting
* hyperparameter optimization with Optuna
* experiment tracking with MLflow
* vector search using Qdrant and FAISS
* retrieval-augmented generation (RAG)
* retrieval benchmarking
* FastAPI service
* Streamlit demo UI
* automated tests
* full pipeline orchestration

---

# Tested Environment

| Component              | Version                 |
| ---------------------- | ----------------------- |
| Python                 | 3.11                    |
| OS                     | Windows / Linux / macOS |
| Vector DB              | Qdrant                  |
| LLM                    | Ollama                  |
| API                    | FastAPI                 |
| Distributed Processing | Apache Spark            |

---

# System Architecture

```
Raw Ocean Data: NOAA + ONC NetCDF
        |
        v
NetCDF Extraction + SHA256 Source Manifest
        |
        v
Bronze Layer
        |
        +-----------------------------+
        |                             |
        v                             v
Spark Harmonization             Metadata Documents
        |                             |
        v                             v
Silver Layer                    Text Chunking
        |                             |
        v                             v
Spark Feature Engineering       SentenceTransformer Embeddings
        |                             |
        v                             v
Gold Feature Table              Qdrant / FAISS Vector Index
        |                             |
        v                             v
XGBoost Forecasting             Vector Search
        |                             |
        v                             v
Optuna + MLflow Tracking        RAG Context Retrieval
        |                             |
        v                             v
FastAPI /predict + /metrics     FastAPI /search + /ask
        |                             |
        +-------------+---------------+
                      |
                      v
              Streamlit Demo UI
```

The system shares a common ingestion pipeline and splits into:

* Forecasting path: Spark → features → XGBoost → prediction API
* RAG path: metadata → embeddings → vector search → QA API

---

# Repository Structure

```
app/
 ├── api/
 ├── core/
 ├── ingestion/
 ├── ml/
 ├── rag/
 ├── retrieval/
 ├── spark_jobs/
 └── main.py

scripts/
 ├── extract_manifest.py
 ├── spark_harmonize.py
 ├── spark_build_features.py
 ├── train_baseline_model.py
 ├── evaluate_model.py
 ├── hyperparameter_search.py
 ├── build_index.py
 ├── run_rag_benchmark.py
 └── run_full_pipeline.py

tests/

configs/
notebooks/

data/
 ├── raw/
 │    ├── onc/
 │    └── noaa/
 ├── bronze/
 ├── silver/
 ├── gold/
 └── manifests/

artifacts/

streamlit_app.py
docker-compose.yml
README.md
requirements.txt
```

---

# Tech Stack

* Python 3.11
* Apache Spark
* XGBoost
* Optuna
* FastAPI
* Streamlit
* Sentence Transformers
* Qdrant / FAISS
* Ollama
* MLflow
* Docker

---

# Results

## Forecasting Metrics

| Metric | Baseline | Tuned   |
| ------ | -------- | ------- |
| RMSE   | 0.00612  | 0.00585 |
| MAE    | 0.00480  | 0.00453 |
| R²    | 0.99990  | 0.99991 |

## RAG Retrieval

* hit@k: 1.0
* term recall: 0.875

---

# Model Interpretation

High accuracy is expected because ocean temperature data is:

* temporally smooth
* highly autocorrelated

Lag-based features (`lag_1`, `lag_3`, `lag_6`) provide strong predictive signal.

A chronological train/test split is used to prevent leakage.

---

# Limitations

* short-term forecasting only
* same-region data
* limited RAG evaluation dataset
* local deployment

---

# Prerequisites

Install:

* Python 3.11
* Docker
* Ollama
* Java (required for Spark)

---

# Install Ollama

Download:

```
https://ollama.com/download
```

Pull model:

```
ollama pull llama3
```

---

# Environment Setup

Create virtual environment:

```
py -3.11 -m venv .venv
```

Activate:

Windows:

```
.\.venv\Scripts\activate
```

Mac/Linux:

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`:

```
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

LLM_PROVIDER=ollama
LLM_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434

DATA_DIR=./data

VECTOR_BACKEND=qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=ocean_metadata

MLFLOW_TRACKING_URI=./artifacts/mlruns
```

---

# Start Required Services

Start Qdrant:

```
docker compose up -d qdrant
```

Open dashboard:

```
http://localhost:6333/dashboard
```

Start Ollama:

```
ollama run llama3
```

---

# Run Full Pipeline

```
python -m scripts.run_full_pipeline
```

---

# Start the API

```
uvicorn app.main:app
```

Open API docs in browser:

```
http://127.0.0.1:8000/docs
```

---

# Start Streamlit Demo (separate terminal)

Run:

```
streamlit run streamlit_app.py
```

Open:

```
http://localhost:8501
```

---

# API Endpoints

* `/health` → service check
* `/predict` → temperature forecasting
* `/metrics` → model + RAG metrics
* `/search` → vector search
* `/ask` → RAG question answering
* `/provenance/{variable}` → data lineage
* `/eval/retrieval` → retrieval evaluation

All endpoints can be tested via:

```
http://127.0.0.1:8000/docs
```

---

# Run Tests

```
python -m pytest -q
```

---

# Reset and Re-run

Delete:

```
data/bronze/
data/gold/
data/index/
data/manifests/
data/silver/
artifacts/
```

Then rerun:

```
python -m scripts.run_full_pipeline
```
