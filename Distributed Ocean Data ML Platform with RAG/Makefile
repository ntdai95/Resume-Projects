.PHONY: manifest harmonize features train evaluate hyperparameters index benchmark clean setup services all api demo test

manifest:
	python -m scripts.extract_manifest

harmonize:
	python -m scripts.spark_harmonize

features:
	python -m scripts.spark_build_features

train:
	python -m scripts.train_baseline_model

evaluate:
	python -m scripts.evaluate_model

hyperparameters:
	python -m scripts.hyperparameter_search

index:
	python -m scripts.build_index

benchmark:
	python -m scripts.run_rag_benchmark

clean:
	rm -rf data/bronze/*
	rm -rf data/silver/*
	rm -rf data/gold/*
	rm -rf data/manifests/*
	rm -rf artifacts/models/*
	rm -rf artifacts/reports/*
	rm -rf artifacts/plots/*

setup:
	pip install -r requirements.txt

services:
	docker compose up -d qdrant

all: manifest harmonize features train evaluate hyperparameters index benchmark

api:
	uvicorn app.main:app

demo:
	streamlit run streamlit_app.py

test:
	python -m pytest -q