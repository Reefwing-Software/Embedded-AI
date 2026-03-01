# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Select columns to plot
columns_to_plot = ['Voltage', 'Average Voltage', 'Current', 'Average Current', 'Temperature', 'SOC']

# Create a box plot for each selected column
plt.figure(figsize=(12, 6))
data[columns_to_plot].boxplot()
plt.title('Box Plot of Input Features and SOC')
plt.ylabel('Value')
plt.grid(True)
plt.show()