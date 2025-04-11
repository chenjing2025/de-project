terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  credentials = "C:\\Program Files (x86)\\GCP_Credentials\\dtc-de-course-447820-299db174bd40.json"
  project     = "dtc-de-course-447820"  # Replace this with your actual Google Cloud project ID
  region      = "us-central1"
}

resource "google_storage_bucket" "data-lake-bucket"  {
  name          = "my-deproject-data-bucket"  # Replace this with your unique bucket name
  location      = "US"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # days
    }
  }

  force_destroy = true
}

# Uncomment and modify this block when you are ready to define a BigQuery dataset
resource "google_bigquery_dataset" "dataset" {
 dataset_id = "my_project_dataset" 
 project    = "dtc-de-course-447820" 
 location   = "US"
 }
