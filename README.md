# 🚴‍♂️ End-to-End Data Pipeline for Santander Bike Rentals

## 📑Table of Contents
* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Cloud Setup](#cloud-setup)
  * [Provision GCP Resources with Terraform](#provision-gcp-resources-with-terraform)
  * [Set Up Airflow with Docker](#set-up-airflow-with-docker)
* [Data Pipeline Setup](#data-pipeline-setup)
  * [Data Ingestion with Airflow DAG](#data-ingestion-with-airflow-dag)
  * [Data Transformation with DBT Cloud](#data-transformation-with-dbt-cloud)
* [Dashboard Setup](#dashboard-setup)
* [Running the Pipeline](#running-the-pipeline)

## Overview
This guide will walk you through setting up an end-to-end data pipeline using Apache Airflow, Google Cloud Storage (GCS), BigQuery, and Looker Studio. By the end of this workshop, you'll have a working dashboard visualizing London Santander bike rental data.

## Problem Statement
The goal of this project is to:

✅ Automate data ingestion from TfL (Transport for London) open data.

✅ Store raw data in Google Cloud Storage (GCS) as a data lake.

✅ Load and transform data into Google BigQuery for analytics.

✅ Build a dashboard in Looker Studio to visualize bike rental trends.

## Cloud Setup
### Provision GCP Resources with Terraform
First, we need to create a Google Cloud Storage bucket and a BigQuery dataset.

🛠 Step 1: Install Terraform

+ Install Terraform on your system by following this guide:[Terraform Installation Guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/windows.md).

+ Once installed, verify the installation with:

```
terraform -v  # Check Terraform version
```

🛠 Step 2: Google Cloud SDK and Credentials Setup

+ Set up the Google Cloud SDK on your system and authenticate with your Google Cloud project.

+ Follow the setup instructions here:
[Google Cloud SDK Setup Guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md#initial-setup)


🛠 Step 3: Create a Terraform Script 

+ Create a file called main.tf in a designated folder for your Terraform projects. For example, create a folder like C:\Users\user\terraform-projects.

+ You can refer to your main.tf file [here](https://github.com/chenjing2025/de-zcamp/blob/main/terraform_basic/main.tf).


🛠 Step 4: Deploy Terraform 

+ Open your terminal or command prompt and run the following commands:

```
C:\Users\user>cd C:\Users\user\terraform-projects
C:\Users\user\terraform-projects>terraform init
C:\Users\user\terraform-projects>terraform plan
C:\Users\user\terraform-projects>terraform apply
```

+ These [commands](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/1_terraform_overview.md#execution-steps)
will:

1. Initialize Terraform (terraform init).

2. Preview the changes Terraform will make (terraform plan).

3. Apply the changes to your Google Cloud project (terraform apply).


### Set Up Airflow with Docker
🛠 Step 1: Install Docker in WSL (Ubuntu)

Ensure Docker is installed and running inside WSL. You could verify installation:
```
docker --version
docker run hello-world
```

🛠 Step 2: Install Apache Airflow using Docker

1. Create an Airflow project directory

```
mkdir ~/airflow && cd ~/airflow
```
2. Download the official docker-compose.yaml file

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.2/docker-compose.yaml'
```
3. Set environment variables
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
4. Initialize Airflow
```
docker compose up airflow-init
```
5. Start Airflow in detached mode
```
docker compose up -d
```
6. Check running containers
```
docker ps
```
7. Access Airflow Web UI

Open a browser and go to: http://localhost:8080

+ **Default credentials**:

  + Username: airflow
 
  + Password: airflow

🛠 Step 3: Open Airflow Project in VS Code (WSL)

1. Open WSL and navigate to the Airflow directory
```
cd ~/airflow
```
2. Launch VS Code in the Airflow directory
```
code .
```
This will open the project in VS Code Remote - WSL.

You can start creating DAGs inside ~/airflow/dags/


## Data Pipeline Setup

🛠 Step 1: Configure Airflow

Before you can run Airflow, ensure that the environment is properly configured.

1. Access the Airflow Webserver Container

To configure Airflow inside the container, first execute the following command to get inside the Airflow webserver container:
```
docker exec -it airflow-airflow-webserver-1 bash
```
2. Switch to the Airflow User
   
Airflow should be run by the airflow user for proper permissions. Switch to the airflow user inside the container:
```
su - airflow
```
3. Install Python Dependencies

Some additional Python packages are required, like apache-airflow-providers-google for GCP integration.
```
pip install apache-airflow-providers-google
```

4. Set Up Google Cloud Credentials
```
nano ~/.bashrc
export GOOGLE_APPLICATION_CREDENTIALS="/mnt/d/GCP_Credentials/dtc-de-course-447820-299db174bd40.json"
source ~/.bashrc
```

5. Verify the Environment Variable
```
echo $GOOGLE_APPLICATION_CREDENTIALS
```
   
🛠 Step 2: Create Your First DAG

Now that your environment is configured, it's time to create your first DAG.

1. Create a DAG File

Inside the ~/airflow/dags/ directory, create a Python file for your first DAG:

```
nano ~/airflow/dags/test_hello_dag.py
```

2. Define the DAG

Inside the test_hello_dag.py file, define a simple DAG using the PythonOperator. This DAG will run a Python function that prints a message to the console when triggered.

3. Verify the DAG
   
Once you've created the test_hello_dag.py file, Airflow should automatically detect the new DAG. You can verify that it appears in the Airflow Web UI. Go to http://localhost:8080.
You should see test_hello_dag listed in the DAGs tab.

🛠 Step 3: Start Airflow with Docker Compose

1. Navigate to the Airflow directory
```
cd ~/airflow
```
2. Check for docker-compose.yml
```
ls
```
You should see the docker-compose.yml file listed in the directory.

3. Start Airflow containers
```
docker-compose up -d
```
4. Check container status

You can verify that all containers are running:
```
docker ps
```

5. Access Airflow Web UI

Once the containers are running, you can access the Airflow Web UI at http://localhost:8080:

Username: airflow
Password: airflow

6. Edit DAGs or SQL Files

To edit DAGs or SQL scripts, open the Airflow directory in VS Code:
```
code .
```
This will open the Airflow project in VS Code, where you can make changes to the DAGs or any SQL files required for the pipeline.

7. Restart Airflow Services

If you make any changes to the DAGs or configurations, you might need to restart the Airflow webserver or scheduler for the changes to take effect.
```
docker-compose restart airflow-webserver
docker-compose restart airflow-scheduler
```

8. Verify Pipeline in Web UI

After restarting, navigate back to the Airflow Web UI at http://localhost:8080 to monitor and manage the DAGs.

### Data Ingestion with Airflow DAG
🛠 Step 1: Define the DAGs
* Create DAGs for data fetching and loading.
* Use the appropriate operators to handle GCS and BigQuery transfers.
  
**Important:** Ensure that you configure the gcp_conn_id in Airflow UI to establish a connection to your Google Cloud project.
To do this:
  1. Go to the Airflow UI.
  2. Navigate to Admin > Connections.
  3. Add a new connection with the following details:
  ```yaml
  Conn ID: google_cloud_default   
  Conn Type: Google Cloud
  Keyfile JSON: Paste the content of GCP service account JSON key here.
  Project ID: Google Cloud project ID.
  ```
  Click `Save` to save the connection.

🛠 Step 2: Set Task Dependencies
* Ensure the data_ingestion DAG runs first, followed by data_load_to_bq.

🛠 Step 3: Automate and Monitor
* Schedule the DAGs to run automatically using Airflow's scheduler.
* Monitor the tasks and DAGs in the Airflow UI.

### Data Transformation with DBT Cloud
🛠 Step 1: Create a DBT Cloud Account
* Sign up at [getdbt.com](https://www.getdbt.com/).
* After logging in, create a new project and link it to GitHub repository.

🛠 Step 2: Connect to BigQuery
* Navigate to Deploy > Environments > Configure Connection.
* Choose BigQuery as the data platform.
* Provide the following details:
  * GCP Project ID
  * Default Dataset (e.g., my_project_dataset)
  * Location (e.g. US)
  * Authentication using a service account JSON key
* Upload your service account key. Once connected, DBT Cloud will manage your credentials and profiles.yml automatically.

🛠 Step 3: Set Up Your DBT Project
* Use the DBT Cloud IDE (built into the browser) to create your models — no local installation is required.
* Inside the IDE:
  * Navigate to the /models directory.
  * Add new .sql files to define transformations.
  * Use folders to organize models if needed (e.g., /models/staging, /models/core).

🛠 Step 4: Define and Run Models
* In each model .sql file, write a `SELECT` query that transforms your data in BigQuery.
  * Example: `fact_cyclingdata.sql` aggregates cycling trips by mode, path, and location.
* You can run commands directly in the command box at the bottom of the DBT Cloud IDE using:
  * `dbt run` to execute all models or a specific model (e.g., `dbt run --select fact_cyclingdata`). 
* Add tests to your project for data validation (dbt test) using .yml files or test blocks.
* Schedule jobs under the Deploy > Jobs tab to automate runs on a recurring basis or after ingestion.

<img src="images/dbt_lineage.png" width="800">

## Dashboard Setup

1. Open Looker Studio → Click Create Report

2. Select BigQuery as your data source

3. Choose the bike_rentals.dataset.cleaned_table

* Notes:
  * Each chart or table in your report can be linked to a different data source. 
  * You can manually add additional datasets

5. Create visualizations:

- Build at least two visualizations:
    - Bar Chart → Categorical data distribution
    - Line Chart → Bike rentals over time

## Running the Pipeline
To run the entire pipeline:

1️⃣ Start Terraform:

```
terraform apply
```

2️⃣ Start Airflow:

```
docker-compose up -d
```

3️⃣ Trigger DAG in Airflow UI:

Open http://localhost:8080

Run fetch_filtered_data_and_upload_to_gcs. once it completed. Run load_external_and_raw_data_to_bq.

<p align="center">
  <img src="images/dag_ingest_to_gcs.png" alt="Airflow dag_ingest_to_gcs" width="50%" />
  <img src="images/dag_load_to_bq.png" alt="Airflow dag_load_to_bq" width="45%" />
</p>

4️⃣ Check GCS after ingestion and BigQuery after dbt transformed data

<p align="center">
  <img src="images/gcs.png" alt="Airflow dag_ingest_to_gcs" width="50%" />
  <img src="images/bigquery.png" alt="Airflow dag_load_to_bq" width="45%" />
</p>

5️⃣ Open Looker Studio and refresh the dashboard

<img src="images/dashboard.png" width="800">
