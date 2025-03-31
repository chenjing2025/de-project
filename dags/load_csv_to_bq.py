from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow import models
from airflow.utils.dates import days_ago

# Define the parameters
bucket_name = 'my-deproject-data-bucket'  # GCS bucket name
csv_file_path = 'test_cycle/monitoring_locations.csv'  # Path to your CSV file in GCS
project_id = 'dtc-de-course-447820'  # GCP Project ID
dataset_id = 'my_project_dataset'  # BigQuery Dataset ID
table_id = 'monitoring_locations'  # BigQuery Table ID

# Define the BigQuery table schema based on your CSV file columns
schema_fields = [
    {'name': 'Site ID', 'type': 'STRING'},
    {'name': 'Location description', 'type': 'STRING'},
    {'name': 'Borough', 'type': 'STRING'},
    {'name': 'Functional area for monitoring', 'type': 'STRING'},
    {'name': 'Road type', 'type': 'STRING'},   
    {'name': 'Latitude', 'type': 'FLOAT'},
    {'name': 'Longitude', 'type': 'FLOAT'}
]

# Define the DAG
with models.DAG(
    'load_csv_to_bq',
    default_args={'owner': 'airflow', 'start_date': days_ago(1)},
    schedule_interval=None,
) as dag:

    # Task: Load the CSV from GCS to BigQuery
    load_csv_to_bq = GCSToBigQueryOperator(
        task_id='load_csv_to_bq',
        bucket=bucket_name,  # GCS bucket name
        source_objects=[csv_file_path],  # Path to the CSV file in GCS
        destination_project_dataset_table=f'{project_id}.{dataset_id}.{table_id}',  # BigQuery destination
        schema_fields=schema_fields,  # Schema of the CSV file
        write_disposition='WRITE_TRUNCATE',  # Overwrite the table on each load
    )
