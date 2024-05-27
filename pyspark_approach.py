import os.path

import yaml
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, monotonically_increasing_id
# from ydata_synthetic.synthesizers.regular import RegularSynthesizer
# from ydata_synthetic.synthesizers import ModelParameters, TrainParameters
# from sklearn.preprocessing import StandardScaler
import numpy as np


def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def create_spark_session(app_name="SyntheticDataGenerator"):
    return SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()


def generate_table_data(table):
    filename = f'{table}' + '.csv'
    full_csv_path = os.path.join('./input_data/',filename)
    df = pd.read_csv(full_csv_path)
    return df


def main():
    config = load_config('config.yaml')
    tables_config = config['tables']
    relationships_config = config['relationships']

    spark = create_spark_session()
    tables_data = {}
    generated_data = {}

    # Step 1: Generate data for each table
    for table in sorted(tables_config, key=lambda x: x['order']):
        table_name = table['name']
        synthetic_df = generate_table_data(table_name)

        # Convert to Spark DataFrame
        spark_df = spark.createDataFrame(synthetic_df)
        #print(spark_df.count())
        tables_data[table_name] = spark_df

    # Step 2: Adjust to ensure referential integrity
    for relationship in relationships_config:
        from_table = relationship['from_table']
        from_column = relationship['from_column']
        to_table = relationship['to_table']
        to_column = relationship['to_column']

        if relationship['type'] == 'one_to_many':
            from_df = tables_data[from_table]
            to_df = tables_data[to_table]

            unique_keys = from_df.select(from_column).distinct().rdd.flatMap(lambda x: x).collect()
            to_df = to_df.withColumn(to_column, lit(None).cast(from_df.schema[from_column].dataType))

            # @udf(from_df.schema[from_column].dataType)
            # def random_key():
            #     return np.random.choice(unique_keys)
            #
            # to_df = to_df.withColumn(to_column, random_key())

            tables_data[to_table] = to_df

        # Add more relationship types handling if needed

    # Save generated data to CSV files
    for table_name, df in tables_data.items():
        df.show(10,truncate=False)
        #df.write.csv(f"{table_name}.csv", header=True, mode='overwrite')


if __name__ == '__main__':
    main()
