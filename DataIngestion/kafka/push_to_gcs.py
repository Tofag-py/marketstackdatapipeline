from google.cloud import storage

def test_gcs_authentication():
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

if __name__ == "__main__":
    test_gcs_authentication()