# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define constants
R = 1  # Resistance in ohms
C = 1  # Capacitance in farads
T = R * C  # Time constant
V_s = 1  # Supply voltage in volts

# Generate time values from 0 to 5T
time = np.linspace(0, 5 * T, 500)

# Capacitor current formula
current = (V_s / R) * np.exp(-time / T)

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the current curve
plt.plot(time, current, label='Current Curve', color='blue')

# Add ticks for the x-axis at specific time constants
plt.xticks([0, 0.7*T, 1*T, 4*T, 5*T], ['0', '0.7T', '1T', '4T', '5T'])

# Add ticks for the y-axis at specific current values
i_max = V_s / R
plt.yticks([0.37 * i_max, 0.5 * i_max, i_max], ['0.37*i', '0.5*i', 'V_s/R'])

# Label the axes
plt.xlabel('Time (t)')
plt.ylabel('Current (i)')
plt.axvline(x=4*T, color='magenta', linestyle='--', label='Transient/Steady State Boundary')

# Title of the plot
plt.title('Capacitor Charge Current vs Time')

# Set the axes limits
plt.xlim(0, 5*T)
plt.ylim(0, i_max)

# Add grid lines
plt.grid(True)

# Display the plot
plt.show()