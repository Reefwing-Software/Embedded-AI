# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import cvxpy as cp
import scipy.fftpack as spfft
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6_v5")
image_name = 'two_sine_waves.pdf'
image_path = os.path.join(image_folder, image_name)

# Create the sum of two sinusoids for Middle C (C4) and G (G4)
n = 5000  # number of samples
t = np.linspace(0, 1, n)  # time vector, 1 second

# Frequencies for Middle C (C4) and G (G4)
f_c4 = 261.63  # Frequency of Middle C (C4) in Hz
f_g4 = 392.00  # Frequency of G (G4) in Hz

# Signal: sum of sinusoids at middle C and G
y = np.sin(2 * np.pi * f_c4 * t) + np.sin(2 * np.pi * f_g4 * t)

# Perform the Discrete Cosine Transform (DCT)
yt = spfft.dct(y, norm='ortho')

# Create subplots with 1 row and 2 columns (side by side)
fig, axs = plt.subplots(1, 2, figsize=(12, 4))  # 1 row, 2 columns

# Plot the original signal (Time Domain) in the first subplot
axs[0].plot(t, y, color='0.4')  # Plot in gray
axs[0].set_title("Sum of Two Sinusoids: Middle C and G", fontproperties=prop)
axs[0].set_xlabel("Time [s]", fontproperties=prop)
axs[0].set_ylabel("Amplitude", fontproperties=prop)
axs[0].grid(True, color='0.8')  # Light gray grid
axs[0].set_xlim([0.0, 0.15])  # Set the x-axis limit to be between 0.0 and 0.15 seconds

# Plot the DCT coefficients (Frequency Domain) in the second subplot
axs[1].plot(yt, color='0.4')  # Plot in gray
axs[1].set_title("DCT of Sum of Two Sinusoids (Middle C and G)", fontproperties=prop)
axs[1].set_xlabel("Frequency Bin", fontproperties=prop)
axs[1].set_ylabel("DCT Coefficient", fontproperties=prop)
axs[1].grid(True, color='0.8')  # Light gray grid
axs[1].set_xlim([0, 1250])  # Set the x-axis limit to between 0 and 1.25 kHz

# Adjust layout to avoid overlapping titles/labels
plt.tight_layout()

# Display the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()

# Perform the Augmented Dickey-Fuller test
adf_result = adfuller(y)

# Extract and display the results
print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])
print("Critical Values:", adf_result[4])

# Interpretation of the result
if adf_result[1] < 0.05:
    print("The time series is stationary (reject the null hypothesis)")
else:
    print("The time series is non-stationary (fail to reject the null hypothesis)")

# Random 10% sample of y(t)
sample_size = int(n * 0.1)
random_indices = np.random.choice(n, size=sample_size, replace=False)
random_indices.sort()
compressed_signal = y[random_indices]
compressed_time = t[random_indices]

image_name = 'f09013.pdf'
image_path = os.path.join(image_folder, image_name)

# Create an IDCT matrix for the full signal (based on the identity matrix)
A_full_idct = spfft.idct(np.identity(n), norm='ortho', axis=0)

# Sample the rows of the IDCT matrix corresponding to the compressed signal indices
A = A_full_idct[random_indices]

# Define the L1 minimization problem in terms of the DCT coefficients
# vx represents the DCT coefficients we want to optimize
vx = cp.Variable(n)
objective = cp.Minimize(cp.norm(vx, 1))  # Minimize the L1 norm of DCT coefficients
constraints = [A @ vx == compressed_signal]  # Ensure the reconstructed signal matches compressed samples
problem = cp.Problem(objective, constraints)

# Solve the L1 minimization problem
result = problem.solve(verbose=True)

# Reconstruct the signal from the optimized DCT coefficients
reconstructed_dct = np.array(vx.value)
reconstructed_dct = np.squeeze(reconstructed_dct)

# Perform inverse DCT to reconstruct the signal in the time domain
reconstructed_signal = spfft.idct(reconstructed_dct, norm='ortho')
reconstructed_signal_dct = spfft.dct(reconstructed_signal, norm='ortho')

# Plot the reconstructed signal in time domain and its DCT (side by side)
fig, axs = plt.subplots(1, 2, figsize=(12, 4))  # 1 row, 2 columns

# First subplot: Reconstructed signal in time domain
axs[0].plot(t, reconstructed_signal, color='0.5')
axs[0].set_title("Reconstructed Signal (Time Domain)", fontproperties=prop)
axs[0].set_xlabel("Time [s]", fontproperties=prop)
axs[0].set_ylabel("Amplitude", fontproperties=prop)
axs[0].grid(True, color='0.8')
axs[0].set_xlim([0, 0.15])  # Set x-axis to 0 to 0.15 seconds
axs[0].set_ylim([-2, 2])  # Set y-axis to -2 to 2

# Second subplot: DCT of the reconstructed signal
axs[1].plot(reconstructed_signal_dct, color='0.5')
axs[1].set_title("DCT of Reconstructed Signal", fontproperties=prop)
axs[1].set_xlabel("Frequency Bin", fontproperties=prop)
axs[1].set_ylabel("DCT Coefficient", fontproperties=prop)
axs[1].grid(True, color='0.8')
axs[1].set_xlim([0, 1250])  # Set x-axis limit to 0 to 1250 frequency bins

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()

# Mean Squared Error (MSE)
mse = mean_squared_error(y, reconstructed_signal)

# Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y, reconstructed_signal)

# Peak Signal-to-Noise Ratio (PSNR)
# First, calculate the maximum possible pixel value of the signal
max_signal_value = np.max(y)
psnr = 20 * np.log10(max_signal_value / np.sqrt(mse))

# Output the results
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"MAE: {mae}")
print(f"PSNR: {psnr} dB")
