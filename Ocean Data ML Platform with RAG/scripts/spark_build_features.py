from app.spark_jobs.session import get_spark
from app.spark_jobs.features import build_temperature_features


def main():
    spark = get_spark("spark-build-features")
    df = spark.read.parquet("data/silver/harmonized_observations.parquet")
    feat = build_temperature_features(df)
    if "time_ts" in feat.columns:
        feat = feat.orderBy("dataset_id", "time_ts")

    feat.write.mode("overwrite").parquet("data/gold/temperature_features.parquet")
    print("Wrote gold features")
    spark.stop()


if __name__ == "__main__":
    main()