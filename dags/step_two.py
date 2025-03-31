from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow import models
from airflow.utils.dates import days_ago

# Define the parameters
project_id = 'dtc-de-course-447820'  # GCP Project ID
dataset_id = 'my_project_dataset'  # BigQuery Dataset ID for the staging table
raw_table_id = 'raw_monitoring_locations'  # Temporary BigQuery Table ID
final_table_id = 'monitoring_locations'  # Final BigQuery Table ID
gcs_raw_table_id = 'gs://my-deproject-data-bucket/test_cycle/monitoring_locations.csv'  # GCS URI

# Define the path to the SQL file
load_raw_sql_file_path = '/opt/airflow/dags/sql/load_raw_data.sql'

# Read the SQL file into a variable
with open(load_raw_sql_file_path, 'r') as f:
    load_raw_sql = f.read()  # Now the variable holds the SQL query

# Define the configuration for BigQuery Job
configuration = {
    "query": {
        "query": load_raw_sql,  # Use the correct variable name here
        "useLegacySql": False,  # Use standard SQL
        "parameters": [
            {"name": "project_id", "parameterType": {"type": "STRING"}, "parameterValue": {"value": project_id}},
            {"name": "dataset_id", "parameterType": {"type": "STRING"}, "parameterValue": {"value": dataset_id}},
            {"name": "raw_table_id", "parameterType": {"type": "STRING"}, "parameterValue": {"value": raw_table_id}},
            {"name": "gcs_raw_table_id", "parameterType": {"type": "STRING"}, "parameterValue": {"value": gcs_raw_table_id}},
        ],
    }
}

# Define the DAG
with models.DAG(
    'load_raw_data_to_bq',
    default_args={'owner': 'airflow', 'start_date': days_ago(1)},
    schedule_interval=None,
) as dag:

    # Task: Execute SQL to load raw data into the temporary table
    load_raw_data_to_bq = BigQueryInsertJobOperator(
        task_id='load_raw_data_to_bq',
        configuration=configuration,  # Pass the configuration
    )
