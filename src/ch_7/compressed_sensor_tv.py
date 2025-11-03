# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import cvxpy as cp

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12) 

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_7")
image_name = 'cs_tv.pdf'
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

# Reconstruct signal using Total Variation Minimization
def reconstruct_signal(num_samples, compressed_samples):
    # Extract the compressed samples and normalize them
    y = np.array(list(compressed_samples.values()))  # Compressed measurements
    y_mean = np.mean(y)
    y_std = np.std(y)
    y_normalized = (y - y_mean) / y_std  # Normalize measurements to mean 0 and std 1
    
    # Create a random Gaussian measurement matrix (for simplicity)
    Phi = np.random.randn(len(y), num_samples)
    
    # TV minimization problem
    x = cp.Variable(num_samples)
    objective = cp.Minimize(cp.tv(x))  # Minimize total variation
    constraints = [Phi @ x == y_normalized]  # Use normalized measurements
    
    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    # De-normalize the reconstructed signal back to the original range
    reconstructed_signal = x.value * y_std + y_mean
    
    return reconstructed_signal

# Plot the original and reconstructed signals in grayscale
def plot_signals(regular_samples, reconstructed_signal):
    num_samples = len(regular_samples)
    time = np.arange(num_samples)

    plt.figure(figsize=(10, 6))

    # Plot the regular samples in a dark gray shade
    plt.plot(time, regular_samples, label='Original Signal', marker='o', color='0.3')  # Dark gray
    # Plot the reconstructed samples in a lighter gray shade
    plt.plot(time, reconstructed_signal, label='Reconstructed Signal', linestyle='--', marker='x', color='0.6')  # Lighter gray

    # Apply font from prop to title and labels
    plt.title('Original vs Reconstructed Signal', fontproperties=prop)
    plt.xlabel('Sample Number', fontproperties=prop)
    plt.ylabel('Temperature (°C)', fontproperties=prop)

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
    if reconstructed_signal is None:
        print("Error: Reconstructed signal is None!")
    
    # Plot the original and reconstructed signals
    plot_signals(regular_samples, reconstructed_signal)