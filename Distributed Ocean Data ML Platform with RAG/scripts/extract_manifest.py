from pathlib import Path
import pandas as pd, jsonlines
from app.ingestion.hashing import sha256_file
from app.ingestion.netcdf_extract import extract_netcdf_to_frames


RAW_DIR = Path("data/raw")
BRONZE_DIR = Path("data/bronze")
MANIFEST_PATH = Path("data/manifests/source_manifest.jsonl")

def main():
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    if MANIFEST_PATH.exists(): 
        MANIFEST_PATH.unlink()

    all_obs, all_meta = [], []
    for source_dir in [RAW_DIR/"onc", RAW_DIR/"noaa"]:
        for file_path in source_dir.glob("*.nc"):
            obs_df, meta_df = extract_netcdf_to_frames(file_path)
            dataset_id = source_dir.name
            with jsonlines.open(MANIFEST_PATH, mode="a") as writer:
                writer.write({"dataset_id": dataset_id,
                              "file_path": str(file_path),
                              "sha256": sha256_file(file_path),
                              "variables": meta_df.iloc[0]["variables"],
                              "coordinates": meta_df.iloc[0]["coordinates"],
                              "attrs": meta_df.iloc[0]["attrs"]})
                
            if not obs_df.empty:
                obs_df["dataset_id"] = dataset_id; all_obs.append(obs_df)

            meta_df["dataset_id"] = dataset_id; all_meta.append(meta_df)

    if all_obs: 
        pd.concat(all_obs, ignore_index=True).to_parquet(BRONZE_DIR/"observations.parquet", index=False)

    if all_meta: 
        pd.concat(all_meta, ignore_index=True).to_parquet(BRONZE_DIR/"metadata.parquet", index=False)

    print("Wrote bronze parquet and manifest")


if __name__ == "__main__": 
    main()
