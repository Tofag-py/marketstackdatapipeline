#!/bin/bash

# Navigate to the directory containing your Python script
cd DataIngestion/ingestion.py

# Source conda setup script
source /Users/tofag/anaconda3/etc/profile.d/conda.sh

# Activate conda environment
conda activate Tofag3.10

# Run the Python script
python ingestion.py
