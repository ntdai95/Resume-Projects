from app.spark_jobs.session import get_spark
from app.spark_jobs.harmonize import harmonize_observations


def main():
    spark = get_spark("spark-harmonize")
    df = spark.read.parquet("data/bronze/observations.parquet")
    out = harmonize_observations(df)
    out.write.mode("overwrite").parquet("data/silver/harmonized_observations.parquet")
    print("Wrote silver parquet")
    spark.stop()


if __name__ == "__main__": 
    main()
