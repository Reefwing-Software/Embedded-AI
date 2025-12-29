# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import json
import requests

# Path to credentials file
credentials_file = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/credentials/edge-impulse-api-key.json")

# Edge Impulse parameters
PROJECT_ID = "577219"  # Replace with your Project ID
JOB_ID = "27200445"    # Replace with the Job ID of interest
BASE_URL = "https://studio.edgeimpulse.com/v1/api"
LOG_DOWNLOAD_URL = f"{BASE_URL}/{PROJECT_ID}/jobs/{JOB_ID}/stdout"

# Function to load the API key from JSON file
def load_api_key(file_path):
    """
    Loads the API key from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            credentials = json.load(f)
        api_key = credentials.get("api_key")
        if api_key:
            print(f"Retrieved API Key: {api_key}")  # Confirm API key
        else:
            print("API key not found in the credentials file.")
        return api_key
    except Exception as e:
        print(f"Error loading API key: {e}")
        return None

# Function to download job logs
def download_job_log(api_key, save_path):
    """
    Downloads the job log from Edge Impulse API and saves it locally.
    """
    headers = {"x-api-key": api_key}

    try:
        print(f"Requesting job logs for Project ID: {PROJECT_ID}, Job ID: {JOB_ID}...")
        response = requests.get(LOG_DOWNLOAD_URL, headers=headers)

        if response.status_code == 200:
            # Save logs to a file
            with open(save_path, "w") as f:
                f.write(response.text)
            print(f"Job log saved to: {save_path}")

            # Print a preview
            print("\n--- Job Log Preview ---")
            for i, line in enumerate(response.text.splitlines()):
                if i >= 20:  # Show only the first 20 lines
                    print("... [Log truncated]")
                    break
                print(line.strip())
        else:
            print(f"Failed to download logs. Status code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"An error occurred while downloading logs: {e}")

# Main Execution
if __name__ == "__main__":
    # Load API key
    API_KEY = load_api_key(credentials_file)
    if not API_KEY:
        print("Failed to load API key. Please check the credentials file.")
        exit(1)

    # Output file path
    output_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_13/")
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"job_{JOB_ID}_stdout_log.txt")

    # Download job logs
    download_job_log(API_KEY, output_file)