# Copyright (c) 2026 David Such
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
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6_v5")
image_name = 'f06005.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_6")
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

# Reconstruct signal using compressed samples
def reconstruct_signal(num_samples, compressed_samples):
    reconstructed_signal = np.zeros(num_samples)
    
    # Sort the compressed samples by index to ensure they are in order
    sorted_samples = sorted(compressed_samples.items())

    # Extract the indices and values from sorted samples
    sample_indices = [index for index, _ in sorted_samples]
    sample_values = [value for _, value in sorted_samples]

    # Fill the known compressed samples into the reconstructed signal
    for index, value in sorted_samples:
        reconstructed_signal[index] = value

    # Start the interpolation from the first compressed sample
    first_index = sample_indices[0]
    
    # Fill the values before the first compressed sample with its value
    reconstructed_signal[:first_index] = sample_values[0]

    # Interpolate the values between known compressed samples
    for i in range(len(sample_indices) - 1):
        start_index = sample_indices[i]
        end_index = sample_indices[i + 1]
        start_value = sample_values[i]
        end_value = sample_values[i + 1]
        
        # Linearly interpolate between start and end
        for j in range(start_index + 1, end_index):
            reconstructed_signal[j] = start_value + (end_value - start_value) * (j - start_index) / (end_index - start_index)

    # Fill in any remaining values after the last compressed sample with its value
    last_index = sample_indices[-1]
    reconstructed_signal[last_index:] = sample_values[-1]

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
    