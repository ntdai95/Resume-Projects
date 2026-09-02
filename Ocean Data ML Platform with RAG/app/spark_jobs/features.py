from pyspark.sql import functions as F, Window


def build_temperature_features(df):
    temp_df = df.filter(F.col("canonical_variable") == "sea_water_temperature")
    if "time" in temp_df.columns:
        temp_df = temp_df.withColumn("time_ts", F.to_timestamp("time"))
        temp_df = temp_df.filter(F.col("time_ts").isNotNull())
        temp_df = temp_df.withColumn("hour", F.hour("time_ts"))
        temp_df = temp_df.withColumn("dayofyear", F.dayofyear("time_ts"))
        w = Window.partitionBy("dataset_id").orderBy("time_ts")
        temp_df = temp_df.withColumn("lag_1", F.lag("normalized_value", 1).over(w))
        temp_df = temp_df.withColumn("lag_3", F.lag("normalized_value", 3).over(w))
        temp_df = temp_df.withColumn("lag_6", F.lag("normalized_value", 6).over(w))
    else:
        w = Window.partitionBy("dataset_id").orderBy(F.monotonically_increasing_id())
        temp_df = temp_df.withColumn("lag_1", F.lag("normalized_value", 1).over(w))
        temp_df = temp_df.withColumn("lag_3", F.lag("normalized_value", 3).over(w))
        temp_df = temp_df.withColumn("lag_6", F.lag("normalized_value", 6).over(w))
        temp_df = temp_df.withColumn("hour", F.lit(None).cast("int"))
        temp_df = temp_df.withColumn("dayofyear", F.lit(None).cast("int"))

    return temp_df.dropna(subset=["lag_1", "lag_3", "lag_6"])