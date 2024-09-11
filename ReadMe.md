# Real-Time Market Data Pipeline

## Project Overview

The Real-Time Market Data Pipeline is a comprehensive data engineering project designed to handle real-time data ingestion, processing, and analytics. This project leverages Apache Kafka for stream processing, Google Cloud Storage (GCS) for data storage, Google BigQuery for data warehousing, Power BI for analytics, and Grafana for monitoring. Prefect is used for orchestrating the data workflows.

## Architecture and Components

### Data Migration
- **Source:** Market data APIs.
- **Ingestion:** Data is ingested using Kafka. A cron job periodically pushes data to Kafka topics.
- **Kafka Setup:**
  - **Topics:** Define Kafka topics for different data streams.
  - **Producers:** Producers push data to Kafka topics.
  - **Consumers:** Consumers read data from Kafka topics and push it to GCS.

### Stream Processing
- **Kafka Streams:** Handle real-time data processing and transformation.

### Data Storage
- **Google Cloud Storage (GCS):** Acts as the data lake for storing raw and processed data. Data is organized into buckets for easy retrieval and management.

### Data Warehouse
- **Google BigQuery:** Used for storing and querying large datasets. Data from GCS is loaded into BigQuery for structured storage and analysis.

### Analytics
- **Power BI:** Connects to Google BigQuery for creating interactive dashboards and reports. Provides insights and visualizations based on the ingested data.

### Orchestration
- **Prefect:** Manages and schedules the data pipelines. Handles the workflow of data ingestion, processing, and transfer between components.

### Monitoring
- **Grafana:** Used for monitoring and visualizing system performance and metrics. Connects to Google Cloud Monitoring for real-time dashboards.

## Setup and Configuration

### Google Cloud Setup

1. **Enable Required APIs:**
   - Compute Engine API
   - Google Cloud Storage API
   - BigQuery API
   - Cloud Monitoring API

2. **Create Service Account:**
   - Create a service account with roles: `Storage Admin`, `BigQuery Admin`, and `Dataflow Admin`.
   - Download the JSON key file and place it in `ConfigFiles/marketstack_ingress.json`.

3. **Terraform Configuration:**
   - **Initialize Terraform:**
     ```bash
     terraform init
     ```
   - **Apply Configuration:**
     ```bash
     terraform apply
     ```

### Kafka Configuration

1. **Setup Kafka Topics:** Define and configure Kafka topics for data streams.
2. **Configure Producers and Consumers:**
   - Implement Kafka producers to push data to topics.
   - Implement Kafka consumers to pull data from topics and process it.

### Data Processing and Storage

1. **Run Data Ingestion Script:**
   ```bash
   python DataIngestion/kafka/push_to_gcs.py

Data Manipulation: Transform and clean data as required before loading into BigQuery.
Data Warehouse Integration
Load Data into BigQuery: Use Dataflow or custom scripts to load processed data from GCS to BigQuery.
Analytics and Visualization
Power BI Setup: Connect Power BI to BigQuery and create dashboards and reports for data visualization.
Orchestration and Monitoring
Prefect:
Create and configure Prefect tasks and flows to Schedule and monitor the data pipeline tasks.
Grafana:
Set up Grafana dashboards to monitor system metrics and performance.
Integrate with Google Cloud Monitoring for real-time data visualization.
Troubleshooting
Permissions Issues: Ensure service accounts have correct roles and permissions.
API Errors: Verify API configurations and enablements.
Data Transfer Issues: Check logs for errors in Kafka, GCS, and BigQuery integration.

**Contributing**
If you wish to contribute to this project, please follow these guidelines:

Fork the Repository:
Create a Feature Branch:
Make Changes:
Submit a Pull Request:

**License**
This project is licensed under the MIT License.

**Contact**
For any questions or issues, please contact .
