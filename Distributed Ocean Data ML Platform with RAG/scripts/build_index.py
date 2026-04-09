from pathlib import Path
import jsonlines
from app.retrieval.index_builder import build_index
from app.core.settings import settings


def load_docs():
    docs = []
    mp = Path("data/manifests/source_manifest.jsonl")
    if mp.exists():
        with jsonlines.open(mp) as reader:
            for row in reader:
                docs.append({"doc_id": row["sha256"],
                             "dataset_id": row["dataset_id"],
                             "source_file": row["file_path"],
                             "text": f"Dataset {row['dataset_id']} from {row['file_path']}. Variables: {', '.join(row['variables'])}"})
                
    metrics = Path("artifacts/reports/model_metrics.json")
    if metrics.exists():
        docs.append({"doc_id": "model-metrics",
                     "dataset_id": "model",
                     "source_file": str(metrics),
                     "text": "Model metrics: " + metrics.read_text()})
        
    return docs


def main():
    build_index(load_docs(), settings.embedding_model)
    print("Built index")


if __name__ == "__main__": 
    main()
