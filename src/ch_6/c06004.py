# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import seaborn as sns


# Load the data
data = pd.read_csv(file_path)

# Pair plot for selected features
sns.pairplot(data[['Voltage', 'Current', 'Temperature', 'SOC']])
plt.show()