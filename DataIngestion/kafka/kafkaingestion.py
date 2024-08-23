from confluent_kafka import Producer, Consumer
import json
import sys
from pathlib import Path
from prefect import task, flow

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Add parent directory to sys.path
from ingestion import load_config, fetch_data, merge_data, load_existing_data  # Import necessary functions

def read_config():
    # Construct the full path to the client.properties file
    config_path = Path("kafka/client.properties")
    
    config = {}
    with open(config_path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.split('=', 1)
                config[parameter.strip()] = value.strip()
    return config

@task
def create_producer(config):
    producer = Producer(config)
    return producer

@task
def create_consumer(config):
    consumer = Consumer(config)
    return consumer

@task
def produce_message(producer, topic, data):
    """Push data to Kafka"""
    # Convert data to JSON string if it's not already a string
    data_str = json.dumps(data) if not isinstance(data, str) else data
    
    # Produce message
    producer.produce(topic, value=data_str)
    producer.flush()

@task
def consume_message(topic, config, timeout=10):
    """Consume messages from Kafka with a timeout."""
    config["group.id"] = "MarketStack1"
    config["auto.offset.reset"] = "earliest"
    consumer = Consumer(config)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout)
            if msg is None:
                print("No more messages or timeout reached. Exiting...")
                break
            if msg.error() is None:
                print(f"Consumed message: {msg.key()} - {msg.value()}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

@flow
def kafka_flow():
    """Main Kafka flow."""
    config = read_config()
    topic = "IngestData"
    
    # Load the API configuration
    api_config = load_config()
    api_key = api_config.get('api_key')
    url = (f"http://api.marketstack.com/v1/eod?access_key={api_key}&symbols=AAPL"
           f"&date_from=2020-01-01&date_to=2024-12-31&sort=DESC")
    
    # Load existing data
    existing_data = load_existing_data('../data/output_data.json')
    
    # Fetch new data
    new_data = fetch_data(api_key, url)
    
    # Merge the existing and new data
    merged_data = merge_data(existing_data, new_data)
    
    # Produce the merged data to Kafka
    producer = create_producer(config)
    produce_message(producer, topic, merged_data)
    
    # Consume messages from Kafka
    consume_message(topic, config)

if __name__ == "__main__":
    kafka_flow()
