# Use the official Airflow image as base
FROM apache/airflow:2.8.2

# Switch to root user to install system dependencies
USER root

# Install system dependencies required for dbt and dbt-bigquery
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Switch to the airflow user to install Python dependencies
USER airflow

# Upgrade pip and install dbt and dbt-bigquery together
RUN pip install --upgrade pip \
    && pip install --no-cache-dir dbt dbt-bigquery

# Set the working directory
WORKDIR /opt/airflow

# Copy your DAGs, logs, config, and plugins
COPY dags/ /opt/airflow/dags
COPY logs/ /opt/airflow/logs
COPY config/ /opt/airflow/config
COPY plugins/ /opt/airflow/plugins
