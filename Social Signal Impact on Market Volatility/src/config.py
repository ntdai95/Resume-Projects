from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    data_raw: Path
    data_processed: Path
    data_reports: Path
    figs: Path
    models: Path


def get_paths() -> Paths:
    repo_root = Path(__file__).resolve().parents[1]
    data_raw = repo_root / "data" / "raw"
    data_processed = repo_root / "data" / "processed"
    data_reports = repo_root / "data" / "reports"
    figs = data_reports / "figs"
    models = repo_root / "models"
    for p in [data_raw, data_processed, data_reports, figs, models]:
        p.mkdir(parents=True, exist_ok=True)

    return Paths(repo_root, data_raw, data_processed, data_reports, figs, models)


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str
    user: str
    password: str
    database: str


def get_neo4j_config() -> Neo4jConfig:
    return Neo4jConfig(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "neo4jproject"),
        database=os.getenv("NEO4J_DATABASE", "stock-influencer-tweets-neo4j"),
    )
