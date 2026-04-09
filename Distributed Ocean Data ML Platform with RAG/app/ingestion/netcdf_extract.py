import xarray as xr
import pandas as pd
from pandas.api.types import is_numeric_dtype


def _normalize_time_like_columns(df):
    for col in df.columns:
        if col.lower() in {"time", "timestamp", "datetime"}:
            df[col] = df[col].astype(str)
        elif df[col].dtype == "object":
            sample = df[col].dropna()
            if not sample.empty:
                first = sample.iloc[0]
                module_name = type(first).__module__
                if "cftime" in module_name:
                    df[col] = df[col].astype(str)

    return df


def extract_netcdf_to_frames(file_path):
    ds = xr.open_dataset(file_path, engine="netcdf4")
    obs_frames = []
    skipped_variables = []
    for var in ds.data_vars:
        df = ds[[var]].to_dataframe().reset_index()
        df = _normalize_time_like_columns(df)
        if not is_numeric_dtype(df[var]):
            skipped_variables.append(var)
            continue

        df = df.rename(columns={var: "value"})
        df["source_variable"] = var
        df["source_file"] = str(file_path)
        df["units"] = ds[var].attrs.get("units")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["value"])
        obs_frames.append(df)

    obs_df = pd.concat(obs_frames, ignore_index=True) if obs_frames else pd.DataFrame()
    meta_df = pd.DataFrame([
        {
            "source_file": str(file_path),
            "variables": ",".join(list(ds.data_vars)),
            "numeric_variables": ",".join([v for v in ds.data_vars if v not in skipped_variables]),
            "skipped_variables": ",".join(skipped_variables),
            "coordinates": ",".join(list(ds.coords)),
            "attrs": str(dict(ds.attrs)),
        }
    ])

    return obs_df, meta_df