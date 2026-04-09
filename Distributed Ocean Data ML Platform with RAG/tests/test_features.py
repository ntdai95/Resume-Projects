import os
import sys
from pyspark.sql import SparkSession
from app.spark_jobs.features import build_temperature_features


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

def test_features():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    rows = [{"dataset_id": "onc",
             "canonical_variable": "sea_water_temperature",
             "normalized_value": float(i),
             "time": "2024-01-01 00:00:00",
             "source_variable": "temp",
             "units": "K",
             "normalized_unit": "degC",
             "source_file": "a",
             "provenance_transform": "x"} for i in range(1, 10)]
    
    df = spark.createDataFrame(rows)
    assert build_temperature_features(df).count() >= 1
    spark.stop()
