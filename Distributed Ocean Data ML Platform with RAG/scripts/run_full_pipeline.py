import subprocess
import sys


STEPS = [
    ("Extract manifest", [sys.executable, "-m", "scripts.extract_manifest"]),
    ("Spark harmonize", [sys.executable, "-m", "scripts.spark_harmonize"]),
    ("Build Spark features", [sys.executable, "-m", "scripts.spark_build_features"]),
    ("Train baseline model", [sys.executable, "-m", "scripts.train_baseline_model"]),
    ("Evaluate baseline model", [sys.executable, "-m", "scripts.evaluate_model"]),
    ("Hyperparameter search", [sys.executable, "-m", "scripts.hyperparameter_search"]),
    ("Build vector index", [sys.executable, "-m", "scripts.build_index"]),
    ("Run retrieval benchmark", [sys.executable, "-m", "scripts.run_rag_benchmark"]),
]


def main():
    for name, cmd in STEPS:
        print(f"\n=== {name} ===")
        print(" ".join(cmd))
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            raise SystemExit(f"Step failed: {name}")

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()