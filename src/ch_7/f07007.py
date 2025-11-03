# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12) 

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_7")
image_name = 'f07007.pdf'
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

# Function to reconstruct the staircase signal based on compressed samples
def reconstruct_signal(num_samples, compressed_samples):
    # Sort compressed_samples by sample index (key) to ensure the proper order
    sorted_samples = sorted(compressed_samples.items())

    # Create an array to hold the reconstructed signal
    reconstructed_signal = np.zeros(num_samples)
    
    # Get the sorted x (time/index) and y (values)
    x_samples = [x for x, y in sorted_samples]
    y_samples = [y for x, y in sorted_samples]
    
    # Set all values up to the first compressed sample to its value
    current_value = y_samples[0]  # Initial value from the first compressed sample
    for i in range(x_samples[0] + 1):
        reconstructed_signal[i] = current_value  # Fill from 0 to x_samples[0] with the first value

    # Iterate through the number of samples to fill in the staircase values
    for i in range(x_samples[0], num_samples):
        # Find which interval the current index belongs to and assign the corresponding y value
        if i >= x_samples[-1]:
            reconstructed_signal[i] = y_samples[-1]
        else:
            for j in range(len(x_samples) - 1):
                if x_samples[j] <= i < x_samples[j + 1]:
                    reconstructed_signal[i] = y_samples[j]
                    break

    return reconstructed_signal

# Plot the original and reconstructed signals in grayscale
def plot_signals(regular_samples, reconstructed_signal):
    num_samples = len(regular_samples)
    time = np.arange(num_samples)

    plt.figure(figsize=(10, 6))

    # Plot the regular samples in a dark gray shade
    plt.plot(time, regular_samples, label='Original signal', marker='o', color='0.3')  # Dark gray
    # Plot the reconstructed samples in a lighter gray shade
    plt.plot(time, reconstructed_signal, label='Reconstructed signal', linestyle='--', marker='x', color='0.6')  # Lighter gray

    # Plot the compressed samples on top of the reconstructed signal
    compressed_sample_indices = list(compressed_samples.keys())
    compressed_sample_values = list(compressed_samples.values())
    plt.scatter(compressed_sample_indices, compressed_sample_values, color='0.4', label='Compressed samples', 
            marker='D', edgecolor='0.2', linewidths=2, zorder=5)

    # Apply font from prop to title and labels
    plt.title('Original vs reconstructed signal', fontproperties=prop)
    plt.xlabel('Sample number', fontproperties=prop)
    plt.ylabel('Temperature (degrees)', fontproperties=prop)

    # Apply font to the legend and plot in grayscale
    plt.legend(prop=prop)

    plt.grid(True, color='0.8')  # Light gray grid

    # Show plot
    plt.tight_layout()
    plt.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.show()

# Main function
if __name__ == '__main__':
    # Assign Arduino sensor data from file
    regular_samples, compressed_samples = read_arduino_output(file_path)

    # Reconstruct the signal using compressed samples
    num_samples = len(regular_samples)
    reconstructed_signal = reconstruct_signal(num_samples, compressed_samples)
    
    # Plot the original and reconstructed signals
    plot_signals(regular_samples, reconstructed_signal)

    # Mean Squared Error (MSE)
mse = np.mean((regular_samples - reconstructed_signal) ** 2)

# Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)

# Mean Absolute Error (MAE)
mae = np.mean(np.abs(regular_samples - reconstructed_signal))

# Peak Signal-to-Noise Ratio (PSNR)
psnr = 10 * np.log10(np.max(regular_samples) ** 2 / mse)

# Print results
print(f'MSE: {mse}')
print(f'RMSE: {rmse}')
print(f'MAE: {mae}')
print(f'PSNR: {psnr}')