# ETL Scripts (Data Creation)

This folder contains one-time data ingestion scripts used to create
the SQLite and Neo4j databases used by the project.

These scripts are NOT required to run the offline pipeline.
They are preserved for data provenance and reproducibility.

Output artifacts:

- data/raw/StocksTraining.db
- data/raw/StocksTesting.db
- data/raw/stock_influencer_tweets.db
- data/raw/stock-influencer-tweets-neo4j.dump
