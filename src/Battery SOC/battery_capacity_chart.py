# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt

# Data from the table
capacity = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]
voltage_3S = [12.6, 12.45, 12.33, 12.25, 12.07, 11.96, 11.86, 11.74, 11.63, 11.56, 11.51, 11.46, 11.39, 11.36, 11.28, 11.24, 11.18, 11.12, 11.06, 10.98, 9.82]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(capacity, voltage_3S, marker='o', linestyle='-', color='b', label='3S Battery')

# Adding labels and title
plt.xlabel('Capacity (%)')
plt.ylabel('Voltage (V)')
plt.title('Capacity vs Voltage for 3S Battery')
plt.legend()
plt.grid(True)

# Reversing the x-axis
plt.gca().invert_xaxis()

# Display the plot
plt.show()