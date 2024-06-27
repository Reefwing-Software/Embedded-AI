# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define time constant T (in arbitrary units)
T = 1

# Generate time values from 0 to 5T
time = np.linspace(0, 5 * T, 500)

# Capacitor charging voltage formula
voltage = 1 - np.exp(-time / T)

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the charging curve
plt.plot(time, voltage, label='Capacitor Voltage', color='blue')

# Add ticks for the x-axis at specific time constants
plt.xticks([0, 0.7*T, 1*T, 2*T, 3*T, 4*T, 5*T], ['0', '0.7T', '1T', '2T', '3T', '4T', '5T'])

# Add ticks for the y-axis at specific voltage percentages
plt.yticks([0.5, 0.63, 1], ['0.5V_s', '0.63V_s', 'V_s'])

# Label the axes
plt.xlabel('Time Constant (T)')
plt.ylabel('Capacitor Voltage (V_s)')

# Title of the plot
plt.title('Capacitor Charging Curve')

# Add a horizontal line to indicate the transient period from 0T to 4T at 0.2 V_s
plt.hlines(0.2, 0, 4*T, colors='red', linestyles='dotted', linewidth=2)
plt.annotate('', xy=(0, 0.2), xytext=(4*T, 0.2), arrowprops=dict(arrowstyle='<->', color='red'))
plt.text(2*T, 0.25, 'Transient Period', horizontalalignment='center', color='red')

plt.axvline(x=4*T, color='magenta', linestyle='--', label='Transient/Steady State Boundary')

# Add a dotted line to indicate the steady state period from 4T onwards at 0.2 V_s with arrowheads
plt.hlines(0.2, 4*T, 5*T, colors='green', linestyles='dotted', label='Steady State Period', linewidth=2)
plt.annotate('', xy=(4*T, 0.2), xytext=(5*T, 0.2), arrowprops=dict(arrowstyle='->', color='green'))
plt.annotate('', xy=(5*T, 0.2), xytext=(4*T, 0.2), arrowprops=dict(arrowstyle='->', color='green'))
plt.text(4.5*T, 0.25, 'Steady State', horizontalalignment='center', color='green')

# Add grid lines
plt.grid(True)

# Move the y-axis to x=0
plt.gca().spines['left'].set_position('zero')
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.gca().yaxis.tick_left()
plt.gca().set_xlim(left=0)

# Show the legend
plt.legend(loc='right')

# Display the plot
plt.show()