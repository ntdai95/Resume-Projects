# Resume Projects

Personal and class projects that I keep on my resume. Each one has its own README
with the methods, the numbers and what did not work.

## Projects

| Project | What it is |
|---|---|
| [Ocean Data ML Platform with RAG](./Ocean%20Data%20ML%20Platform%20with%20RAG) | A pipeline that ingests raw NetCDF ocean sensor data from two independent providers, harmonizes it with Apache Spark, trains an XGBoost temperature forecaster, and exposes a retrieval-augmented question-answering interface over the resulting metadata. FastAPI service, Qdrant vector store, Docker Compose. **[Demo with live responses from every endpoint](./Ocean%20Data%20ML%20Platform%20with%20RAG#demo)** |
| [Distributed Facility Reservation System](./Distributed%20Facility%20Reservation%20System) | 27 versioned REST endpoints with published OpenAPI documentation, 71 pytest tests across the API, database and reservation rules, and one booking contract negotiated with four other teams. Built at UChicago in a team of 4. |
| [Stock Sentiment Analysis](./Stock%20Sentiment%20Analysis) | Pairs tweet sentiment from six financial influencers with daily prices for ten technology stocks, then tests the relationship with correlation, Granger causality and GARCH. Sentiment tracks same-day moves and says more about volatility than about the next day's return. Neo4j and SQLite, FinTwitBERT, statsmodels and arch. |
| [Parallel Image Processing Engine](./Parallel%20Image%20Processing%20Engine) | An image processing engine in Go supporting grayscale, sharpening, blurring and edge detection through custom 2D convolution kernels, with sequential, fan-in/fan-out and bulk synchronous parallel execution models. |
