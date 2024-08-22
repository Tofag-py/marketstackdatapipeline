import requests
import yaml
import json
import pandas as pd
import os
from prefect import task, flow

@task
def load_config(filename='../ConfigFiles/apikeys.yaml'):
    """Load API key from YAML file."""
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

@task
def fetch_data(api_key, symbols='AAPL', sort='DESC', date_from=None, date_to=None, limit=100, offset=0):
    """Fetch data from the API using the provided API key and parameters."""
    url = "http://api.marketstack.com/v1/eod"
    params = {
        'access_key': api_key,
        'symbols': symbols,
        'sort': sort,
        'date_from': date_from,
        'date_to': date_to,
        'limit': limit,
        'offset': offset
    }
    
    # Remove parameters that are None
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"Error occurred: {err}")
        return None

@task
def download_data_locally(data):
    """Append new data to existing files and preview it."""
    # Define file paths
    json_file_path = './data/output_data.json'
    csv_file_path = './data/output_data.csv'
    
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    
    # Append data to JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            existing_data = json.load(file)
        if 'data' in existing_data and 'data' in data:
            existing_data['data'].extend(data['data'])
        else:
            existing_data = data
    else:
        existing_data = data

    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
    print(f"Data has been appended to {json_file_path}.")

    # Optionally append data to CSV file (if it is tabular)
    if 'data' in data:
        if os.path.exists(csv_file_path):
            df_existing = pd.read_csv(csv_file_path)
            df_new = pd.DataFrame(data['data'])
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = pd.DataFrame(data['data'])
        
        df_combined.to_csv(csv_file_path, index=False)
        print(f"Data has been appended to {csv_file_path}.")

    # Load data for preview
    preview_size = 5  # Number of records to preview
    if 'data' in data:
        preview_data = data['data'][:preview_size]
        print("Preview of fetched data:")
        for record in preview_data:
            print(record)
    else:
        print("No data available for preview.")

@flow
def main_flow():
    """Main flow to fetch and process data."""
    config = load_config()
    api_key = config.get('api_key')
    
    # Define parameters
    symbols = 'AAPL'  # Example symbol
    sort = 'DESC'
    date_from = '2024-01-01'  # Optional
    date_to = '2024-01-31'    # Optional
    limit = 100
    offset = 0
    
    data = fetch_data(api_key, symbols, sort, date_from, date_to, limit, offset)
    if data:
        download_data_locally(data)

if __name__ == '__main__':
    main_flow()
