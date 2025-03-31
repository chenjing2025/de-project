import requests
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow import models
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import tempfile

# Function to download file from the URL and upload it to GCS
def download_and_upload_to_gcs(url, bucket_name, destination_blob_name):
    # Step 1: Download file from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Step 2: Save the file to a temporary location on the local system
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file.close()
            # Step 3: Upload the file to Google Cloud Storage using GCSHook
            hook = GCSHook()
            hook.upload(bucket_name, destination_blob_name, temp_file.name)
            print(f"File uploaded to {bucket_name}/{destination_blob_name}")
    else:
        raise Exception(f"Failed to download the file. Status code: {response.status_code}")

# Define the DAG
with models.DAG(
    'fetch_data_and_upload_to_gcs',
    default_args={'owner': 'airflow', 'start_date': days_ago(1)},
    schedule_interval=None,
) as dag:
    
    # Define the URL and GCS parameters
    file_url = 'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/1%20Monitoring%20locations.csv'
    bucket_name = 'my-deproject-data-bucket'  # Replace with your GCS bucket name
    destination_blob_name = 'test_cycle/monitoring_locations.csv'  # GCS path

    # Task to fetch data from URL and upload to GCS
    upload_task = PythonOperator(
        task_id='download_and_upload_to_gcs',
        python_callable=download_and_upload_to_gcs,
        op_args=[file_url, bucket_name, destination_blob_name],
    )
