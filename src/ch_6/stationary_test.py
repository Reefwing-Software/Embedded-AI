# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm


# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=13) 

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_7")
image_name = 'cs_stationary_test.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_7")
file_name = "compressed_sensor_data.txt"
file_path = os.path.join(data_folder, file_name)

# Function to read sensor data from a text file
def read_arduino_output(filename):
    regular_samples = []
    compressed_samples = {}
    reading_compressed = False
    reading_regular = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Ignore empty lines or lines that don't contain 'Sample'
            if not line or "Sample" not in line:
                continue

            if "Compressed Samples" in line:
                reading_compressed = True
                reading_regular = False
                continue
            elif "All Regular Samples" in line:
                reading_regular = True
                reading_compressed = False
                continue

            # Safely split and handle potential errors
            try:
                parts = line.split(":")
                index = int(parts[0].split()[1])  # Extract index (e.g., "Sample 7:")
                value = float(parts[1].strip().split()[0])  # Extract temperature value (e.g., "23 °C")

                if reading_compressed:
                    compressed_samples[index] = value
                elif reading_regular:
                    regular_samples.append(value)

            except (IndexError, ValueError) as e:
                # Print or log any problematic lines for debugging
                print(f"Error processing line: {line}, Error: {e}")
    
    return regular_samples, compressed_samples

def plot_results(regular_samples):
    # Step 1: Plot the time series (Visual Inspection)
    plt.figure(figsize=(10, 6))
    plt.plot(regular_samples, label='Temperature Time Series')
    plt.title('Temperature Time Series')
    plt.xlabel('Sample Index')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()

    # Step 2: Rolling statistics (rolling mean and variance)
    window_size = 10
    rolling_mean = pd.Series(regular_samples).rolling(window=window_size).mean()
    rolling_std = pd.Series(regular_samples).rolling(window=window_size).std()

    plt.figure(figsize=(10, 6))
    plt.plot(regular_samples, label='Original')
    plt.plot(rolling_mean, label=f'Rolling Mean (window={window_size})', color='red')
    plt.plot(rolling_std, label=f'Rolling Std (window={window_size})', color='black')
    plt.legend(loc='best')
    plt.title('Rolling Mean and Standard Deviation')
    plt.grid(True)
    plt.show()

    # Step 3: ADF Test
    adf_test = adfuller(regular_samples)
    print('ADF Statistic: %f' % adf_test[0])
    print('p-value: %f' % adf_test[1])
    print('Critical Values:')
    for key, value in adf_test[4].items():
        print('\t%s: %.3f' % (key, value))

    if adf_test[1] < 0.05:
        print("The time series is stationary.")
    else:
        print("The time series is non-stationary.")

# Main function
if __name__ == '__main__':
    # Assign Arduino sensor data from file
    regular_samples, compressed_samples = read_arduino_output(file_path)
    
    plot_results(regular_samples)