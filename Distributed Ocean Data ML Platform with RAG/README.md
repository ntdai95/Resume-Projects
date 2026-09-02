# Distributed Ocean Data ML Platform with RAG

An end-to-end pipeline that ingests raw NetCDF ocean sensor data from two
independent providers, harmonizes it with Apache Spark, trains an XGBoost
temperature forecaster, and exposes a retrieval-augmented question-answering
interface over the resulting metadata. A FastAPI service and Streamlit demo
sit on top.

```bash
pip install -r requirements.txt
docker compose up -d qdrant
python -m scripts.run_full_pipeline
uvicorn app.main:app
```

---

## Headline result

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Naive persistence (predict = previous reading) | **0.00442** | **0.00198** | **0.99990** |
| XGBoost, default params | 0.01172 | 0.00871 | 0.99932 |
| XGBoost, tuned (Optuna, 25 trials) | 0.00710 | 0.00527 | 0.99975 |

Tuning cuts RMSE by about 39% over the default model, but neither XGBoost
run beats the trivial baseline of repeating the last reading. **Read this
alongside the caveat below** — an R² of 0.9997 looks like a strong forecaster
in isolation, and only looks ordinary once it's checked against a model that
learns nothing at all.

---

## The persistence-baseline caveat

Ocean temperature at a few readings per minute barely moves between
consecutive samples, so `lag_1` (the previous reading) is already close to
the physical ceiling on this task. The XGBoost models have that same
`lag_1` value as an input feature, so this isn't a case of the baseline
having information the model lacks. Rather, a tree ensemble approximates a
near-identity function with a finite set of leaf-value outputs, which
introduces a discretization error that copying the previous value exactly
does not have. On a signal this smooth, that quantization error costs more
than a few trees' worth of interaction terms and lag/time features gain
back.

This project keeps the comparison in the README on purpose. A model
metrics report with only the XGBoost numbers would read as a successful
forecaster; checked against persistence, it's evidence that short-horizon
temperature forecasting on this data has very little headroom over "assume
no change," and that headroom is the honest thing to report.

---

## Does a longer horizon or more sensors change the story?

The one-step result above raises an obvious follow-up: does XGBoost close
the gap at a longer forecast horizon, where "assume no change" should
eventually run out of room? And does giving the model the site's other
sensors — salinity and dissolved oxygen, sampled at the same mooring —
help it forecast temperature? `scripts/horizon_experiment.py` tests both:
at seven horizons from 1 second to 2 hours, it trains one XGBoost model on
temperature's own lags and time features, and a second with salinity and
oxygen added, and compares both to persistence under the same chronological
split.

| Horizon | Persistence RMSE | XGBoost (temp only) RMSE | XGBoost (+ salinity, oxygen) RMSE |
|---|---|---|---|
| 1 s | 0.004 | 0.008 | 0.009 |
| 30 s | 0.038 | 0.048 | 0.060 |
| 5 min | 0.094 | 0.281 | 0.322 |
| 15 min | 0.153 | 0.334 | 0.376 |
| 30 min | 0.211 | 0.440 | 0.436 |
| 1 hr | 0.286 | 0.425 | 0.557 |
| 2 hr | 0.392 | 0.681 | 0.714 |

Persistence wins at every horizon tested, and the gap widens rather than
closes. At 1 and 2 hours out, both XGBoost variants post a **negative R²**
(-1.40 for temperature-only, -1.64 with sensor context) — worse than
predicting the test set's mean. Adding salinity and oxygen makes the model
worse at five of the seven horizons, not better.

This is a coherent result, not noise. The temperature series over this
six-week window behaves like a smooth, near-diffusive process: the current
reading already carries most of the available information about the near
future, and there is little genuine local trend to extrapolate. The
lag-difference trend feature and the cross-sensor context let XGBoost fit
fine-grained patterns in the training period's chronological 80%; at longer
horizons those patterns increasingly describe training-period noise rather
than anything that recurs in the held-out final 20%, so the model's error
compounds while persistence's does not — persistence never had a training
period to overfit in the first place. Full numbers, including MAE and R²
at every horizon, are in `artifacts/reports/horizon_experiment.json`; the
error curve is plotted in `artifacts/plots/horizon_experiment.png`.

The practical conclusion: for this sensor, at these horizons, engineered
features and multi-sensor context measurably hurt point-forecast accuracy
rather than helping. That's a more useful result to publish than either
the original 0.9999 R² or a model that quietly beat a baseline nobody
checked.

---

## Testing the method on a signal that should be forecastable

Everything above says persistence wins because subsurface ocean temperature
is close to a random walk at these sampling rates -- there's no local trend
to extrapolate. That's a claim about the *signal*, not a limitation of
XGBoost or the feature set, and it's worth checking against a series that
has a real, physically obvious predictable component. `scripts/air_temperature_benchmark.py`
runs the identical persistence-vs-XGBoost comparison, at horizons from 1
minute to 24 hours, against air temperature from ONC's [Baynes Sound
meteorological station](https://dap.oceannetworks.ca/erddap/tabledap/scalar_1203278.html)
(same regional network, ~4.5 months at 1-minute resolution, pulled live
from ONC's ERDDAP server rather than the fixed NetCDF snapshots in
`data/raw/`) -- a signal with an obvious deterministic
driver, the daily solar heating cycle, that a naive "assume no change"
forecast has no way to anticipate.

| Horizon | Persistence RMSE | XGBoost (air temp only) | XGBoost (+ pressure, wind) |
|---|---|---|---|
| 1 min | 0.079 | 0.124 | 0.123 |
| 15 min | 0.411 | 0.498 | 0.494 |
| 1 hr | 0.829 | 0.884 | 0.833 |
| 3 hr | 1.640 | 1.217 | 1.171 |
| 6 hr | 2.556 | 1.673 | 1.599 |
| 12 hr | 3.509 | 2.054 | **1.823** |
| 24 hr | 1.460 | 1.957 | 1.531 |

This is the crossover the ocean data never showed. Persistence wins at
sub-hour horizons -- nothing beats "no change" a minute from now -- but
loses decisively from 3 hours out: at 6 and 12 hours its R² is actually
**negative** (-0.57 and -1.95), while XGBoost with pressure and wind stays
positive (0.39 and 0.20) and cuts RMSE by up to 48% at the 12-hour mark.
Persistence partially recovers at exactly 24 hours, because "same time
yesterday" is a genuinely strong forecast for a diurnal signal and none of
this model's features (lags of a few minutes, plus categorical hour/day)
give it an equivalent to that literal day-old reading.

Cross-sensor context helps here, consistently, which is the opposite of
the ocean result: barometric pressure trend is a standard meteorological
predictor of near-term temperature change, so adding it is exploiting a
real physical relationship rather than fitting noise the training period
won't repeat. Full metrics (RMSE, MAE, R² at every horizon) are in
`artifacts/reports/air_temperature_benchmark.json`; the plot is
`artifacts/plots/air_temperature_benchmark.png`.

Together, the two experiments are the actual point: the same pipeline,
unchanged, correctly finds no exploitable structure in one signal and real,
substantial structure in another, for reasons that follow from the physics
of each. That's what "the model works" should mean here -- not a single
headline metric, but a method that gets the right answer on both a
negative and a positive case.

---

## RAG retrieval

The corpus is small by construction -- 6 source files plus 4 experiment
reports (model metrics, hyperparameter search, and both horizon
benchmarks) -- so a retrieval eval here can't claim what a large-scale
benchmark would. It's sized and scored to be honest about that rather than
to produce a clean number: `scripts/run_rag_benchmark.py` runs 10
natural-language questions (not paraphrases of the target labels, and
covering every document at least once) at `top_k=2`, a real filter against
a 10-document corpus rather than the `top_k=5` an earlier version used,
which returned half the corpus on every query regardless of relevance.

| Metric | Value |
|---|---|
| hit@k | 0.9 (9/10) |
| term recall | 0.85 |

The one miss is a legible failure, not noise: asked whether ocean water
temperature's forecast skill changes at longer horizons, the retriever
returned the model-metrics document instead of the horizon-experiment one
-- a reasonable confusion between two documents that are both, in a
shallow sense, "about the model." Full per-query results are in
`artifacts/reports/rag_eval_rows.jsonl`.

This replaced an earlier version of this eval that scored a suspicious
1.0: 4 queries that were near-restatements of the target term (*"which
datasets mention salinity?"*) against a `top_k` that returned most of the
corpus regardless of the question. Fixing it surfaced a real bug along the
way -- `app/rag/runtime.py` built each document's text with
`', '.join(row['variables'])` where `variables` was already a
comma-joined string, not a list, so `join` iterated its characters and
every document advertised its variables as `t, i, m, e, ..., o, x, y, g,
e, n` instead of `time, oxygen_corrected`. It still retrieved correctly
often enough to pass the old eval, which is exactly why the old eval
wasn't testing much. The fix also dropped two attributes the raw NOAA
files carry -- `title` and `institution` -- that turned out to be
generic boilerplate from an unrelated NOAA program and would have made the
retriever's context look wrong to anyone who read it closely.

---

## Bugs found and fixed while building this

The pipeline runs clean now, but it didn't when this pass started. Four
bugs were serious enough to invalidate the numbers above if left in place,
and are worth documenting because none of them threw an error — the code
ran, produced plausible-looking metrics, and was wrong.

**Target leakage via the raw pre-normalization value.** The feature table
included both `value` (the raw measurement, e.g. degrees Kelvin) and the
target `normalized_value` (`value - 273.15`, degrees Celsius). Any model can
recover the target from that feature with one subtraction, which is exactly
why an earlier version of this pipeline reported R² above 0.9999 — it had
memorized arithmetic, not learned a forecast. Fixed by excluding `value`
(and the meaningless positional index `row`) from the feature columns in
both `app/ml/train.py` and `scripts/hyperparameter_search.py`.

**Context columns orphaned from their measurements.** Each NetCDF file
stores `time`, `latitude`, and `longitude` as data variables sharing a
`row` dimension with the actual measurements, not as indexed coordinates.
`extract_netcdf_to_frames` pulled one variable out of the dataset at a time
(`ds[[var]].to_dataframe()`), which silently dropped every row's link back
to its own timestamp and position — `hour` and `dayofyear` were 100% null,
and the chronological sort that the training code was already written to
do never had a real `time_ts` column to sort on. Fixed by extracting the
whole dataset once per file and carrying `time`/`latitude`/`longitude`
alongside each measurement row instead of re-deriving them per variable.

**An entire data source silently excluded.** NOAA's sea-surface
temperature file stores its variable as `TEMP_C` (already in Celsius); ONC's
stores `Temperature` (in Kelvin). The harmonization step's synonym list only
recognized the ONC name, so every NOAA temperature reading — 145k rows —
canonicalized to nothing and never reached the model, despite being counted
in the claimed dataset. Fixed by adding `temp_c` to the synonym list and
generalizing the Celsius/Kelvin normalization so a value already in Celsius
is relabeled rather than double-converted.

**Latitude and longitude as an accidental provider label.** The gold table
combines ONC's Pacific Northwest site (one fixed coordinate) with NOAA's
sea-surface temperature site (a different fixed coordinate, thousands of
kilometers away in the U.S. Virgin Islands) into a single feature table,
and neither `latitude` nor `longitude` was ever excluded from the model's
features. Because the chronological split puts the entire test set inside
one slice of ONC's own history (NOAA's rows sort earlier and land
entirely in training), those two columns carried 94% of the trained
model's feature importance — not because location predicts ocean
temperature in any generalizable way, but because they perfectly encode
which provider produced a row, and the two providers have very different
baseline temperatures. This didn't corrupt the reported test metric,
since every test row shares the same fixed ONC coordinate and the split
is a no-op there, but it broke the live system: `/predict` has no way to
accept a location, so it silently evaluated every request at
`latitude=0, longitude=0` — a point the model never saw in training — and
returned nonsense (27.9°C from inputs around 12.4°C). Found by calling the
deployed endpoint, not by reading the code. Fixed by excluding `latitude`
and `longitude` from the feature columns in both `app/ml/train.py` and
`scripts/hyperparameter_search.py` and retraining: the tuned model's RMSE
is essentially unchanged (0.0071 either way), but the untuned
default-params baseline moved from 0.00823 to 0.01172 once it lost the
shortcut.

A fifth issue was environmental rather than a data bug: on Windows,
importing `mlflow` before `torch` in the same process leaves torch's
`c10.dll` unable to initialize (`WinError 1114`), which broke the RAG
benchmark step specifically because `app.rag.evaluation` imports mlflow
before anything imports the embedding model. Fixed by importing `torch`
first in `app/main.py`, `scripts/run_rag_benchmark.py`, and
`app/retrieval/embedder.py`.

---

## System architecture

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
Spark Feature Engineering       Sentence-Transformer Embeddings
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

One shared ingestion pipeline (raw NetCDF → SHA256-hashed bronze layer →
Spark harmonization) feeds two independent paths: forecasting
(harmonize → feature engineering → XGBoost → `/predict`) and RAG
(metadata → embeddings → vector search → `/ask`).

---

## Repository structure

```
app/
 ├── api/          FastAPI routers: predict, search, ask, metrics, eval, provenance, health
 ├── core/         Settings (.env-driven paths, backend selection)
 ├── ingestion/    NetCDF extraction, SHA256 hashing
 ├── ml/           Training, MLflow experiment tracking
 ├── rag/          Answering, prompt templates, retrieval evaluation, runtime doc loading
 ├── retrieval/    Chunking, embedding, Qdrant/FAISS vector stores, retriever
 ├── spark_jobs/   Harmonization and feature-engineering Spark jobs
 └── main.py

scripts/
 ├── extract_manifest.py       NetCDF -> bronze (observations + metadata + source manifest)
 ├── spark_harmonize.py        bronze -> silver (canonicalize variables, normalize units)
 ├── spark_build_features.py   silver -> gold (lag/time features for temperature)
 ├── train_baseline_model.py   Gold table -> XGBoost baseline, logged to MLflow
 ├── evaluate_model.py         Reload the saved model, recompute metrics
 ├── hyperparameter_search.py  Optuna search over XGBoost params
 ├── build_index.py            Metadata + model-report docs -> vector index
 ├── run_rag_benchmark.py      Retrieval eval (hit@k, term recall)
 ├── horizon_experiment.py       Persistence vs. XGBoost across 7 horizons, with/without sensor context (ocean temperature)
 ├── air_temperature_benchmark.py  Same comparison against ONC's Baynes Sound met station (air temperature)
 └── run_full_pipeline.py      Runs the ingestion-to-RAG steps above in order (the two benchmark scripts above are standalone analyses, run separately)

tests/       7 test modules covering the API, features, hashing, prediction, RAG eval, Spark harmonization, and training
configs/     model_config.yaml (target variable, split fraction, XGBoost params)
notebooks/   Exploratory data checks, model evaluation, RAG demo

data/
 ├── raw/onc/, raw/noaa/   Source NetCDF files (not tracked in git)
 ├── bronze/               Extracted observations + metadata + per-file SHA256 manifest
 ├── silver/               Harmonized: canonical variable names, normalized units
 ├── gold/                 Feature table used for training
 ├── manifests/            source_manifest.jsonl
 └── index/                Persisted FAISS index (when VECTOR_BACKEND=faiss)

artifacts/   MLflow runs, saved models, evaluation reports (tracked in git)
streamlit_app.py
Dockerfile           Builds the API image
docker-compose.yml   qdrant + api services
```

---

## Tech stack

Python 3.11, Apache Spark, XGBoost, Optuna, MLflow, FastAPI, Streamlit,
Sentence Transformers, Qdrant (default) or FAISS, Ollama, Docker.

---

## Data

Two providers, six NetCDF files, ~10.8M raw observations after ingestion:

| Provider | Variable | File | Rows |
|---|---|---|---|
| ONC | Dissolved oxygen | `onc_oxygen.nc` | 3,552,866 |
| ONC | Salinity | `onc_salinity.nc` | 3,547,928 |
| ONC | Temperature (K) | `onc_temperature.nc` | 3,547,928 |
| NOAA | Sea surface temperature (°C) | `noaa_sst.nc` | 145,152 |
| NOAA | Barometric pressure | `noaa_pressure.nc` | 75 |
| NOAA | Wind speed | `noaa_wind.nc` | 145 |

The forecaster targets sea water temperature specifically, combining the
ONC and NOAA temperature series (harmonized to a common `degC` unit) into
one 3,693,068-row feature table spanning 2021-05-05 to 2021-06-15. The
other three variables flow through ingestion and harmonization and are
searchable via `/search` and `/ask`, but are not part of the forecasting
target.

Every raw file is SHA256-hashed on ingestion (`app/ingestion/hashing.py`)
and recorded in `data/manifests/source_manifest.jsonl`, so `/provenance`
can trace any prediction or document back to the exact source file it came
from.

A seventh source, ONC's Baynes Sound meteorological station (~120k rows,
1-minute resolution, pulled live from ONC's public ERDDAP server), backs
the air temperature comparison in `scripts/air_temperature_benchmark.py`.
It's independent of the six files above -- CSV rather than NetCDF, and not
part of the Bronze/Silver/Gold pipeline -- so it isn't in this table or the
SHA256 manifest.

### Where the data comes from

Each NetCDF file carries its own citation in its global attributes, pulled
directly from `data/manifests/source_manifest.jsonl`:

| File | Source |
|---|---|
| `onc_oxygen.nc` | [doi.org/10.34943/922beebb-a573-477a-9b12-8d0d63b977a3](https://doi.org/10.34943/922beebb-a573-477a-9b12-8d0d63b977a3) (Ocean Networks Canada) |
| `onc_salinity.nc`, `onc_temperature.nc` | [doi.org/10.34943/39c52da2-0fd7-46d1-88a3-57d284b78d77](https://doi.org/10.34943/39c52da2-0fd7-46d1-88a3-57d284b78d77) (Ocean Networks Canada) |
| `noaa_pressure.nc`, `noaa_sst.nc` | [fisheries.noaa.gov/.../deep-sea-coral-habitat](https://www.fisheries.noaa.gov/national/habitat-conservation/deep-sea-coral-habitat) (NOAA reference embedded in the file; the underlying dataset is served through [NOAA's ERDDAP](https://www.ncei.noaa.gov/erddap/index.html)) |
| `noaa_wind.nc` | [coastalscience.noaa.gov/.../pmn](https://coastalscience.noaa.gov/monitoring-and-assessments/pmn/) (NOAA reference embedded in the file) |
| Baynes Sound met station (air temperature) | [dap.oceannetworks.ca/erddap/tabledap/scalar_1203278](https://dap.oceannetworks.ca/erddap/tabledap/scalar_1203278.html) (Ocean Networks Canada ERDDAP; `scripts/air_temperature_benchmark.py` downloads this one directly) |

Both networks also expose full search catalogs for finding other stations
or variables: [ONC's ERDDAP](https://dap.oceannetworks.ca/erddap/index.html)
and [NOAA's ERDDAP](https://www.ncei.noaa.gov/erddap/index.html).

---

## Environment setup

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\activate       # Windows
source .venv/bin/activate      # Mac/Linux
pip install -r requirements.txt
```

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

Also requires Docker (for Qdrant), Ollama (`ollama pull llama3`), and a
Java runtime (for Spark).

---

## Running it

```bash
docker compose up -d qdrant       # vector store
ollama run llama3                 # local LLM for /ask
python -m scripts.run_full_pipeline
uvicorn app.main:app              # http://127.0.0.1:8000/docs
streamlit run streamlit_app.py    # http://localhost:8501, separate terminal
```

The API and the vector store are both containerized (`Dockerfile`,
`docker-compose.yml`); Spark, training, and the benchmark scripts are not
-- they're one-off batch jobs, not long-running services, and run directly
against the host Python environment. Once the pipeline above has produced
`data/` and `artifacts/` on the host, `docker compose up -d` starts both
containers, mounting those directories in read-write so the API serves
whatever the host-run pipeline last produced:

```bash
docker compose up -d              # qdrant + the FastAPI service, http://localhost:8000/docs
```

API endpoints: `/health`, `/predict`, `/metrics`, `/search`, `/ask`,
`/provenance/{variable}`, `/eval/retrieval`.

Tests: `python -m pytest -q`.

Horizon/context experiment (needs `data/silver/` populated, from
`run_full_pipeline` or `spark_harmonize` alone): `python -m scripts.horizon_experiment`.

Air temperature benchmark (downloads its own CSV from ONC's ERDDAP server
on first run -- see the script for the source URL):
`python -m scripts.air_temperature_benchmark`.

To rebuild from scratch, delete `data/bronze/`, `data/silver/`,
`data/gold/`, `data/manifests/`, `data/index/`, `artifacts/`, then rerun
`python -m scripts.run_full_pipeline`.

---

## Limitations

- No forecast horizon tested (1 second to 2 hours) beats naive persistence on this ocean temperature sensor; the deployed `/predict` model is a working pipeline, not a genuinely predictive one. (Air temperature at the same regional network does show real skill at 3-12 hour horizons -- see above -- but that comparison isn't wired into the API.)
- One region, six weeks of data for the core ocean pipeline — no test of generalization across seasons or locations. The air temperature comparison covers a different four-and-a-half-month window at a nearby site, not the same period.
- RAG evaluation is 10 hand-written queries over a 10-document corpus, not a large-scale benchmark -- see the caveats in the RAG retrieval section above.
- Single-machine Spark (`local[*]`), not a real cluster.
