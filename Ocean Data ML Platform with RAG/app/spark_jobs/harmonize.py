from pyspark.sql import functions as F


def harmonize_observations(df):
    canonical_var = (
        F.when(F.lower(F.col("source_variable")).isin("temperature","temp","temp_c","water_temp","sea_temp"), F.lit("sea_water_temperature"))
         .when(F.lower(F.col("source_variable")).isin("salinity","salt","practical_salinity"), F.lit("sea_water_salinity"))
         .when(F.lower(F.col("source_variable")).isin("oxygen","dissolved_o2","do"), F.lit("dissolved_oxygen"))
         .otherwise(F.col("source_variable"))
    )
    is_temperature = canonical_var == "sea_water_temperature"
    is_kelvin = F.lower(F.col("units")) == "k"
    is_celsius = F.lower(F.col("units")).isin("c", "degc", "celsius")

    normalized_value = F.when(is_temperature & is_kelvin, F.col("value") - F.lit(273.15)).otherwise(F.col("value"))
    normalized_unit = F.when(is_temperature & (is_kelvin | is_celsius), F.lit("degC")).otherwise(F.col("units"))
    return df.withColumn("canonical_variable", canonical_var).withColumn("normalized_value", normalized_value).withColumn("normalized_unit", normalized_unit).withColumn("provenance_transform", F.lit("canonicalize_and_normalize"))
