from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

class Settings:
    project_root = Path(os.getenv("PROJECT_ROOT", "."))
    data_dir = Path(os.getenv("DATA_DIR", "./data"))
    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts"))
    manifest_path = Path(os.getenv("MANIFEST_PATH", "./data/manifests/source_manifest.jsonl"))
    bronze_metadata_path = Path(os.getenv("BRONZE_METADATA_PATH", "./data/bronze/metadata.parquet"))
    bronze_observations_path = Path(os.getenv("BRONZE_OBSERVATIONS_PATH", "./data/bronze/observations.parquet"))
    silver_harmonized_path = Path(os.getenv("SILVER_HARMONIZED_PATH", "./data/silver/harmonized_observations.parquet"))
    gold_features_path = Path(os.getenv("GOLD_FEATURES_PATH", "./data/gold/temperature_features.parquet"))
    model_path = Path(os.getenv("MODEL_PATH", "./artifacts/models/temperature_forecaster.joblib"))
    temp_model_path = Path(os.getenv("TEMP_MODEL_PATH", "./artifacts/models/tmp_temperature_forecaster.joblib"))
    metrics_report_path = Path(os.getenv("METRICS_REPORT_PATH", "./artifacts/reports/model_metrics.json"))
    rag_eval_report_path = Path(os.getenv("RAG_EVAL_REPORT_PATH", "./artifacts/reports/rag_eval_summary.json"))
    rag_eval_rows_path = Path(os.getenv("RAG_EVAL_ROWS_PATH", "./artifacts/reports/rag_eval_rows.jsonl"))
    prediction_plot_path = Path(os.getenv("PREDICTION_PLOT_PATH", "./artifacts/plots/prediction_vs_actual.png"))
    residual_plot_path = Path(os.getenv("RESIDUAL_PLOT_PATH", "./artifacts/plots/residuals.png"))
    horizon_report_path = Path(os.getenv("HORIZON_REPORT_PATH", "./artifacts/reports/horizon_experiment.json"))
    horizon_plot_path = Path(os.getenv("HORIZON_PLOT_PATH", "./artifacts/plots/horizon_experiment.png"))
    air_temp_report_path = Path(os.getenv("AIR_TEMP_REPORT_PATH", "./artifacts/reports/air_temperature_benchmark.json"))
    air_temp_plot_path = Path(os.getenv("AIR_TEMP_PLOT_PATH", "./artifacts/plots/air_temperature_benchmark.png"))
    embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    vector_backend = os.getenv("VECTOR_BACKEND", "qdrant")
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection = os.getenv("QDRANT_COLLECTION", "ocean_metadata")
    llm_provider = os.getenv("LLM_PROVIDER", "ollama")
    llm_model = os.getenv("LLM_MODEL", "llama3")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "./artifacts/mlruns")
    mlflow_experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "ocean_forecasting_spark")
    mlflow_rag_experiment_name = os.getenv("MLFLOW_RAG_EXPERIMENT_NAME", "ocean_rag_evaluation")
    rag_eval_top_k = int(os.getenv("RAG_EVAL_TOP_K", "5"))


    @classmethod
    def ensure_dirs(cls):
        dirs = [
            cls.artifacts_dir / "models",
            cls.artifacts_dir / "plots",
            cls.artifacts_dir / "reports",
            Path(cls.mlflow_tracking_uri.replace("file:", "")),
            cls.data_dir / "index",
        ]
        
        for path in dirs:
            path.mkdir(parents=True, exist_ok=True)


settings = Settings()