import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging

# Define the patterns
years = ['2023', '2024']
waves = ['W1']  # Fixed as mentioned earlier
areas = ['spring']
regions = ['Central', 'Outer']  # Modify as needed
file_urls = []

# Generate the URLs dynamically
for year in years:
    for wave in waves:
        for area in areas:
            for region in regions:
                # Construct the URL for the CSV file
                file_url = f'https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/{year}%20{wave}%20{area}-{region}.csv'
                file_urls.append(file_url)

# Add any additional static URLs if needed
file_urls.append('https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/1%20Monitoring%20locations.csv')

# Set up the default_args for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 24),
}

# Initialize the DAG
dag = DAG(
    'test_fetch_url_csv',
    default_args=default_args,
    description='A test DAG to fetch CSV URLs and log the results',
    schedule_interval=None,  # This DAG will be triggered manually
    catchup=False
)

# Define a Python function to test the URL fetching and logging
def fetch_and_log_csv_urls(**kwargs):
    for file_url in file_urls:
        # Log the file URL
        logging.info(f"Fetching data from: {file_url}")
        
        # Try fetching the URL
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                logging.info(f"Successfully fetched {file_url}")
            else:
                logging.error(f"Failed to fetch {file_url}. Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"An error occurred while fetching {file_url}: {e}")

# Create a task in the DAG to execute the Python function
fetch_and_log_task = PythonOperator(
    task_id='fetch_and_log_csv_urls',
    python_callable=fetch_and_log_csv_urls,
    provide_context=True,
    dag=dag,
)

# Set the task to run when triggered
fetch_and_log_task
