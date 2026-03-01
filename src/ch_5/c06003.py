# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import scipy.stats as stats

# Extract the 'Voltage', 'Current', and 'SOC' columns
voltage_data = data['Voltage']
current_data = data['Current']
soc_data = data['SOC']

# Create subplots for QN plots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# QN plot for Voltage
res = stats.probplot(voltage_data, dist="norm", plot=axes[0])
axes[0].get_lines()[0].set_color('magenta')
axes[0].get_lines()[1].set_color('magenta')
axes[0].set_title('Quantile-Normal (QN) Plot for Voltage Data')
axes[0].set_xlabel('Theoretical Quantiles')
axes[0].set_ylabel('Sample Quantiles')

# QN plot for Current
res = stats.probplot(current_data, dist="norm", plot=axes[1])
axes[1].get_lines()[0].set_color('orange')
axes[1].get_lines()[1].set_color('orange')
axes[1].set_title('Quantile-Normal (QN) Plot for Current Data')
axes[1].set_xlabel('Theoretical Quantiles')
axes[1].set_ylabel('Sample Quantiles')

# QN plot for SOC
res = stats.probplot(soc_data, dist="norm", plot=axes[2])
axes[2].get_lines()[0].set_color('green')
axes[2].get_lines()[1].set_color('green')
axes[2].set_title('Quantile-Normal (QN) Plot for SOC Data')
axes[2].set_xlabel('Theoretical Quantiles')
axes[2].set_ylabel('Sample Quantiles')

plt.tight_layout()
plt.show()