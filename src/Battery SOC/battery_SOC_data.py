# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import requests
import zipfile
import scipy.io
import pandas as pd
import numpy as np

# URL of the file to download
url = "https://data.mendeley.com/public-files/datasets/cp3473x7xv/files/ad7ac5c9-2b9e-458a-a91f-6f3da449bdfb/file_downloaded"

# Output folder contains the extracted ZIP files
output_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC")
os.makedirs(output_folder, exist_ok=True)

# Download and extract the data set
train_folder = os.path.join(output_folder, "Train")
test_folder = os.path.join(output_folder, "Test")
if not os.path.exists(train_folder) or not os.path.exists(test_folder):
    print("Downloading LGHG2@n10C_to_25degC.zip (56 MB) ... ")
    download_folder = os.path.dirname(output_folder)
    filename = os.path.join(download_folder, "LGHG2@n10C_to_25degC.zip")
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

# Define helper function to read .mat files
def read_mat_files(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".mat"):
            filepath = os.path.join(folder, filename)
            mat_data = scipy.io.loadmat(filepath)
            data.append(mat_data)
    return data

# Create a file datastore for both the training data and the test data
fds_train = read_mat_files(train_folder)
fds_test = read_mat_files(test_folder)

# Read all data in the datastores
train_data_full = fds_train[0]
test_data_full_n10deg = fds_test[0]
test_data_full_0deg = fds_test[1]
test_data_full_10deg = fds_test[2]
test_data_full_25deg = fds_test[3]

# Print the shapes of the data arrays to understand their structure
print("Shape of train_data_full['X']: ", train_data_full['X'].shape)
print("Shape of train_data_full['Y']: ", train_data_full['Y'].shape)
print("Shape of test_data_full_n10deg['X']: ", test_data_full_n10deg['X'].shape)
print("Shape of test_data_full_n10deg['Y']: ", test_data_full_n10deg['Y'].shape)

# Resample the data sets to have one data point every 100 seconds, and compute moving averages
def helper_moving_average(df):
    df = df.iloc[::100, :]
    df["AverageVoltage"] = df["Voltage"].rolling(window=6, min_periods=1).mean()
    df["AverageCurrent"] = df["Current"].rolling(window=6, min_periods=1).mean()
    df = df[["Voltage", "Current", "Temperature", "SOC", "AverageVoltage", "AverageCurrent"]]
    return df

def process_data(X, Y, idx):
    print("Processing data with index range:", idx)
    print("Shape of X:", X.shape)
    print("Shape of Y:", Y.shape)
    df = pd.DataFrame(np.vstack((X[:, idx], Y[idx])).T, columns=["Voltage", "Current", "Temperature", "SOC"])
    return helper_moving_average(df)

idx0 = np.arange(0, 184257)
idx10 = np.arange(184258, 337973)
idx25 = np.arange(337974, 510530)
idxN10 = np.arange(510531, 669956)

train_data_0deg = process_data(train_data_full['X'], train_data_full['Y'], idx0)
train_data_10deg = process_data(train_data_full['X'], train_data_full['Y'], idx10)
train_data_25deg = process_data(train_data_full['X'], train_data_full['Y'], idx25)
train_data_n10deg = process_data(train_data_full['X'], train_data_full['Y'], idxN10)
train_data = pd.concat([train_data_0deg, train_data_10deg, train_data_25deg, train_data_n10deg])

test_data_n10deg = helper_moving_average(pd.DataFrame(np.vstack((test_data_full_n10deg['X'], test_data_full_n10deg['Y'])).T, columns=["Voltage", "Current", "Temperature", "SOC"]))
test_data_0deg = helper_moving_average(pd.DataFrame(np.vstack((test_data_full_0deg['X'], test_data_full_0deg['Y'])).T, columns=["Voltage", "Current", "Temperature", "SOC"]))
test_data_10deg = helper_moving_average(pd.DataFrame(np.vstack((test_data_full_10deg['X'], test_data_full_10deg['Y'])).T, columns=["Voltage", "Current", "Temperature", "SOC"]))
test_data_25deg = helper_moving_average(pd.DataFrame(np.vstack((test_data_full_25deg['X'], test_data_full_25deg['Y'])).T, columns=["Voltage", "Current", "Temperature", "SOC"]))