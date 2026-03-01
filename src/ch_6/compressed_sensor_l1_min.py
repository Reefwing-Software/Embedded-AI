# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import scipy.sparse as sp
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_7")
image_name = 'cs_l1.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_7")
file_name = "compressed_sensor_data.txt"
file_path = os.path.join(data_folder, file_name)

# Function to read sensor data from a text file
def read_arduino_output(filename):
    regular_samples = []
    compressed_samples = {}
    random_indices = []  # To store the indices of compressed samples
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
                    random_indices.append(index)  # Save the compressed sample index
                elif reading_regular:
                    regular_samples.append(value)

            except (IndexError, ValueError) as e:
                # Print or log any problematic lines for debugging
                print(f"Error processing line: {line}, Error: {e}")
    
    return regular_samples, compressed_samples, random_indices

# Reconstruct signal using L1 minimization
def reconstruct_signal(num_samples, compressed_samples):
    # Convert compressed_samples dict to a NumPy array using random_indices
    compressed_samples_array = np.array([compressed_samples[idx] for idx in random_indices])

    # Step 1: Differencing the compressed samples
    # Create the difference for compressed_samples_array (1D array)
    diff_compressed_samples = np.diff(compressed_samples_array)

    # Ensure diff_compressed_samples is a 1D array
    diff_compressed_samples = np.ravel(diff_compressed_samples)  # Flatten to 1D if necessary

    # Step 2: Create a measurement matrix (Phi) that selects the compressed sample indices
    # Adjust the shape to account for the difference in length (use len(random_indices) - 1)
    A = sp.csc_matrix((np.ones(len(random_indices) - 1), (range(len(random_indices) - 1), random_indices[:-1])),
                      shape=(len(random_indices) - 1, num_samples - 1))  # Adjust size for differenced data

    # Ensure that the number of rows in A matches the length of diff_compressed_samples
    assert A.shape[0] == len(diff_compressed_samples), "Mismatch between A rows and diff_compressed_samples length."

    # Step 3: Define the L1 minimization problem on the differenced data
    # The objective is to minimize ||x||_1 subject to A * x = diff_compressed_samples
    result = opt.linprog(np.ones(num_samples - 1), A_eq=A.toarray(), b_eq=diff_compressed_samples, method='highs')

    # Check if the optimization was successful
    if result.success:
        # Step 4: Extract the reconstructed differenced signal (solution)
        diff_reconstructed_signal = result.x
    else:
        print("L1 minimization failed. Solver status:", result.status)
        print("Message:", result.message)
        return None

    # Step 5: Integrating (reversing the difference) to reconstruct the original signal
    # We need an initial value to start the integration (first value of compressed_samples_array)
    reconstructed_signal = np.r_[compressed_samples_array[0], np.cumsum(diff_reconstructed_signal) + compressed_samples_array[0]]

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
    regular_samples, compressed_samples, random_indices = read_arduino_output(file_path)
    print(compressed_samples)

    # Reconstruct the signal using compressed samples
    num_samples = len(regular_samples)
    reconstructed_signal = reconstruct_signal(num_samples, compressed_samples)
    if reconstructed_signal is None:
        print("Error: Reconstructed signal is None!")
    
    # Plot the original and reconstructed signals
    plot_signals(regular_samples, reconstructed_signal)