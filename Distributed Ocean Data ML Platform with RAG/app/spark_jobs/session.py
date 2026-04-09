from pyspark.sql import SparkSession


def get_spark(app_name="ocean-ml-rag-spark"):
    return (SparkSession.builder.appName(app_name).master("local[*]").config("spark.sql.shuffle.partitions", "8").getOrCreate())
