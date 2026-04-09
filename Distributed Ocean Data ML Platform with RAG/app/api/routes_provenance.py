from fastapi import APIRouter
import pandas as pd
from pathlib import Path


router = APIRouter()

@router.get("/provenance/{target_variable}")
def provenance(target_variable):
    p = Path("data/silver/harmonized_observations.parquet")
    if not p.exists():
        return {"rows": [], "message": "run spark harmonization first"}
    
    df = pd.read_parquet(p)
    cols = ["dataset_id", "source_file", "source_variable", "canonical_variable", "provenance_transform"]
    rows = df[df["canonical_variable"] == target_variable][cols].drop_duplicates().head(50).to_dict(orient="records")
    return {"target_variable": target_variable, "rows": rows}
