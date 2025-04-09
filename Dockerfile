# Use the official Airflow image as base
FROM apache/airflow:2.8.2-python3.10

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
    curl \
    libgdal-dev \  
    && rm -rf /var/lib/apt/lists/*  

# Fix permissions for /usr/local/bin so airflow user can write to it
RUN chmod -R 777 /usr/local/bin
    
# Switch to the airflow user to install Python dependencies
USER airflow

# Upgrade pip and install dbt and dbt-bigquery
RUN pip install --upgrade pip && \
    pip install --no-cache-dir dbt dbt-bigquery && \
    rm -rf /home/airflow/.cache

# Ensure dbt is available in the path
ENV PATH="$PATH:/home/airflow/.local/bin"

# Set the working directory
WORKDIR /opt/airflow

# Create a directory for dbt profiles and make sure it's available
RUN mkdir -p /home/airflow/.dbt

# Copy your DAGs, logs, config, and plugins
COPY dags/ /opt/airflow/dags
COPY logs/ /opt/airflow/logs
COPY config/ /opt/airflow/config
COPY plugins/ /opt/airflow/plugins

# Set the entrypoint for the Airflow container
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["webserver"]

# Set the environment variable for dbt profiles directory
ENV DBT_PROFILES_DIR /home/airflow/.dbt
