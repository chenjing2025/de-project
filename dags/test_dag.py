from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define the Python function that will be executed by the task
def print_hello():
    print("Hello from Airflow!")

# Define the DAG
dag = DAG(
    'test_hello_dag',  # Unique identifier for the DAG
    description='A simple test DAG',  # Description of the DAG
    schedule_interval='@once',  # Run once when triggered manually
    start_date=datetime(2025, 3, 23),  # Start date for the DAG
    catchup=False  # Don't run past scheduled instances
)

# Define the task
task_hello = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,  # The function to execute
    dag=dag  # Assign the task to the DAG
)

# Set the task execution order (in this case, there is only one task)
task_hello
