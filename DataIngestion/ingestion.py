import requests
import time
import yaml
from prefect import task, flow
import json
import pandas as pd
from datetime import datetime

@task
def load_config(filename='../ConfigFiles/apikeys.yaml'):
    """Load API key from YAML file."""
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

@task
def fetch_data(api_key, url):
    """Fetch data from the API using the provided API key and URL."""
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"Error occurred: {err}")
        return None

def load_existing_data(file_path):
    """Load existing data from the JSON file."""
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        return existing_data
    except FileNotFoundError:
        return {"data": []}  # Return empty data structure if file does not exist

def save_data(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data has been saved to {file_path}.")

def merge_data(existing_data, new_data):
    """Merge new data with existing data, updating with delta loading."""
    existing_df = pd.DataFrame(existing_data['data'])
    new_df = pd.DataFrame(new_data['data'])

    # Assuming 'date' is the unique key to identify records
    merged_df = pd.concat([existing_df, new_df]).drop_duplicates(subset='date', keep='last')
    merged_data = {"data": merged_df.to_dict(orient='records')}
    return merged_data

@flow
def main_flow():
    """Main flow to periodically fetch and process data."""
    config = load_config()
    api_key = config.get('api_key')
    url = "http://api.marketstack.com/v1/eod?access_key=YOUR_ACCESS_KEY&symbols=AAPL"

    json_file_path = './data/output_data.json'

    while True:
        existing_data = load_existing_data(json_file_path)
        new_data = fetch_data(api_key, url)
        
        if new_data:
            updated_data = merge_data(existing_data, new_data)
            save_data(updated_data, json_file_path)
        
        time.sleep(60)  # Respect API rate limits

if __name__ == '__main__':
    main_flow()
