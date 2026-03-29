# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05013.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Pair plot for selected features with darkgray color palette
g = sns.pairplot(data[['Voltage', 'Current', 'Temperature', 'SOC']], 
                 plot_kws={'color': 'darkgray'},
                 diag_kws={'color': 'darkgray', 'fill': True})

# Apply font properties to the plot titles
for ax in g.axes.flat:
    ax.set_title(ax.get_title(), fontproperties=prop, color='black')
    ax.set_xlabel(ax.get_xlabel(), fontproperties=prop, color='black')
    ax.set_ylabel(ax.get_ylabel(), fontproperties=prop, color='black')

plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()