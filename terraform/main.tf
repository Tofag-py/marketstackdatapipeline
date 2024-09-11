# Specify the Terraform provider
provider "google" {
  credentials = file("../ConfigFiles/marketstack_ingress.json")
  project     = "data-streaming-project-433810"
  region      = "us-central1"
}

# Define a Google Cloud Storage bucket
resource "google_storage_bucket" "marketstack_ingress_lake" {
  name     = "marketstack-data-lake"
  location = "US"

  
}

# Define a Google Compute Engine instance
resource "google_compute_instance" "marketstack_ingress_instance" {
  name         = "ingress-instance"  
  machine_type  = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"  # Ubuntu 22.04 LTS
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ensure a public IP is assigned
    }
  }

  tags = ["web"]

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "Resource Created!" > /var/www/html/index.html
    service apache2 start
  EOF
}
