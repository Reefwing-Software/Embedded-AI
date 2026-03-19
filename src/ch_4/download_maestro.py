# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import tensorflow as tf
from pathlib import Path
import zipfile

# Define the data folder and file name
data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/maestro").expanduser()
file_name = "maestro-v3.0.0-midi.zip"
datasets_folder = data_folder / "datasets"  # Default subdirectory created by TensorFlow
file_path = datasets_folder / file_name  # Adjust to match where the file is actually downloaded
extracted_folder = data_folder / "maestro-v3.0.0"

# Ensure the data folder exists
data_folder.mkdir(parents=True, exist_ok=True)
datasets_folder.mkdir(parents=True, exist_ok=True)  

# Check if the ZIP file already exists
if not file_path.exists():
    print(f"Downloading MAESTRO v3.0.0 dataset to {file_path}...")
    tf.keras.utils.get_file(
        fname=file_name,  # Only the filename
        origin="https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip",
        cache_dir=str(data_folder),  # Use data_folder as cache directory
        extract=False,  # Set extract=False since we will extract manually
    )
    print("Download complete.")

# Extract the ZIP file if the extracted folder does not already exist
if not extracted_folder.exists():
    print(f"Extracting {file_name}...")
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(data_folder)
    print(f"Extraction complete to {extracted_folder}.")
else:
    print(f"The dataset is already extracted at {extracted_folder}.")

# Print statistics about the downloaded files
print("\nDataset Statistics:")
if extracted_folder.exists():
    total_files = 0
    total_size = 0
    midi_files = list(extracted_folder.rglob("*.midi")) + list(extracted_folder.rglob("*.mid"))

    for file in extracted_folder.rglob("*"):
        if file.is_file():
            total_files += 1
            total_size += file.stat().st_size

    print(f"Total number of files: {total_files}")
    print(f"Total size of files: {total_size / (1024 * 1024):.2f} MB")
    print(f"Number of MIDI files: {len(midi_files)}")

    # Print a few example files
    print("\nExample MIDI files:")
    for midi_file in midi_files[:5]:
        print(f"- {midi_file}")
else:
    print("No extracted dataset found.")