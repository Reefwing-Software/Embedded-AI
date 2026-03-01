# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import requests
import zipfile

# URL of the file to download
url = "https://data.mendeley.com/public-files/datasets/cp3473x7xv/files/ad7ac5c9-2b9e-458a-a91f-6f3da449bdfb/file_downloaded"

# Output folder contains the extracted ZIP files
# Define the image folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC")
os.makedirs(data_folder, exist_ok=True)

# Download and extract the data set
train_folder = os.path.join(data_folder, "Train")
test_folder = os.path.join(data_folder, "Test")
if not os.path.exists(train_folder) or not os.path.exists(test_folder):
    print("Downloading LGHG2@n10C_to_25degC.zip (56 MB) ... ")
    download_folder = os.path.dirname(data_folder)
    filename = os.path.join(download_folder, "LGHG2@n10C_to_25degC.zip")
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(data_folder)