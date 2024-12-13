from google.cloud import storage
import json

def test_gcs_authentication():
    """Test Google Cloud Storage authentication and list available buckets."""
    try:
        # Initialize a GCS client
        client = storage.Client()
        
        # List the available buckets in your GCP project
        buckets = list(client.list_buckets())
        
        if buckets:
            print("Authentication successful! Buckets found:")
            for bucket in buckets:
                print(f"- {bucket.name}")
        else:
            print("Authentication successful, but no buckets found.")
    except Exception as e:
        print(f"Authentication failed: {e}")

def upload_to_gcs(bucket_name, file_path, destination_blob_name):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        bucket_name (str): Name of the GCS bucket.
        file_path (str): Path to the file to upload.
        destination_blob_name (str): Destination path in the GCS bucket.
    """
    try:
        # Initialize a GCS client
        client = storage.Client()
        
        # Get the bucket
        bucket = client.bucket(bucket_name)
        
        # Create a blob and upload the file
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to {bucket_name}/{destination_blob_name}.")
    except Exception as e:
        print(f"Failed to upload file to GCS: {e}")

if __name__ == "__main__":
    # Example Usage
    test_gcs_authentication()  # Test GCS authentication
    
    # Define GCS bucket name, file path, and destination blob name
    bucket_name = "marketstack-data-lake"
    file_path = "../data/output_data.json"
    destination_blob_name = "processed_data/output_data.json"
    
    # Upload the file to GCS
    upload_to_gcs(bucket_name, file_path, destination_blob_name)
