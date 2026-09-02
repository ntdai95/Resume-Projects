import os
import sys
from pyspark.sql import SparkSession
from app.spark_jobs.harmonize import harmonize_observations


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

def test_spark_harmonize():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    df = spark.createDataFrame([{"source_variable": "temp",
                                 "value": 300.0,
                                 "units": "K"}])
    
    out = harmonize_observations(df).collect()[0]
    assert out["canonical_variable"] == "sea_water_temperature"
    spark.stop()
