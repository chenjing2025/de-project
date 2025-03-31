import requests
from airflow import DAG
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from requests.exceptions import Timeout
import time

# Define the GCS parameters
bucket_name = 'my-deproject-data-bucket'  # Replace with your GCS bucket name
destination_prefix = 'cycling_data/'  # GCS path prefix for uploaded files

# Define dynamic elements for URL generation
years = [2024]
waves = ['W1']
regions = ['Inner-Part2'] 
base_url = 'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/'

# Function to generate the list of URLs dynamically
def generate_file_urls():
    file_urls = []
    for year in years:
        for wave in waves:
            for region in regions:
                url = f"{base_url}{year}%20{wave}%20spring-{region}.csv"
                file_urls.append(url)
    return file_urls

# Generate the list of file URLs
file_urls = generate_file_urls()

# Initialize GCSHook for interacting with Google Cloud Storage
gcs_hook = GCSHook(gcp_conn_id='google_cloud_default')

def fetch_and_upload_to_gcs(url: str, bucket_name: str, destination_prefix: str):
    """Fetch data from URL and upload to GCS with cleaned filename (without timestamp)."""
    retries = 3
    attempt = 0
    while attempt < retries:
        try:
            # Fetch the data from the URL with a longer timeout
            print(f"Fetching URL: {url}")
            response = requests.get(url, timeout=240, stream=True)  # Increased timeout and streaming download
            response.raise_for_status()  # Check if request was successful

            # Clean up the filename to match the required format
            filename = url.split("/")[-1]
            cleaned_filename = filename.replace('%20', ' ').replace(' ', '_')  # Replace '%20' with spaces and spaces with underscores

            # Generate the final GCS path without a timestamp
            gcs_path = f"{destination_prefix}{cleaned_filename}"
            print(f"GCS path: {gcs_path}")

            # Upload the file in chunks to GCS
            blob = gcs_hook.get_conn().bucket(bucket_name).blob(gcs_path)
            with blob.open("wb") as gcs_file:
                for chunk in response.iter_content(chunk_size=1024*1024):  # 1 MB chunks
                    gcs_file.write(chunk)

            print(f"Successfully uploaded {filename} to gs://{bucket_name}/{gcs_path}")
            break  # Exit loop if successful

        except Timeout:
            # Retry on timeout
            attempt += 1
            print(f"Timeout occurred on attempt {attempt}/{retries}. Retrying in 30 seconds...")
            time.sleep(30)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            # Handle other request exceptions
            print(f"Error fetching data from {url}: {e}")
            break  # Exit loop if error occurs

# Define the Airflow DAG
with DAG(
    'fetch_filtered_data_and_upload_to_gcs',
    description='Fetch data from URLs and upload to GCS with cleaned filenames',
    schedule_interval=None,  # You can set a cron expression for scheduled runs
    start_date=days_ago(1),
    catchup=False,  # Do not backfill
    default_args={
        'retries': 3,  # Retry 3 times if tasks fail
        'retry_delay': timedelta(minutes=5),  # Retry delay in case of failure
    },
) as dag:

    # Iterate over the file URLs and upload each to GCS
    for url in file_urls:
        # Clean the task ID to ensure it's valid
        task_id = f"fetch_and_upload_{url.split('/')[-1]}".replace('%20', '_').replace(' ', '_')

        # Define a PythonOperator for each URL with retries
        fetch_and_upload_to_gcs_task = PythonOperator(
            task_id=task_id,
            python_callable=fetch_and_upload_to_gcs,
            op_args=[url, bucket_name, destination_prefix],
            retries=3,  # Retry on failure
            retry_delay=timedelta(minutes=5),  # Retry after 5 minutes
        )
