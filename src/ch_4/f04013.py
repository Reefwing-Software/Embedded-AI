# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn import svm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04013.pdf'
image_path = os.path.join(image_folder, image_name)

# Create sample data
np.random.seed(0)
X = np.r_[np.random.randn(10, 2) - [2, 2], np.random.randn(10, 2) + [2, 2]]
Y = [0] * 10 + [1] * 10

# Fit the model
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X, Y)

# Get the separating hyperplane
w = clf.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(-5, 5)
yy = a * xx - (clf.intercept_[0]) / w[1]

# Plot the parallels to the separating hyperplane that pass through the support vectors
b = clf.support_vectors_[0]
yy_down = a * xx + (b[1] - a * b[0])
b = clf.support_vectors_[-1]
yy_up = a * xx + (b[1] - a * b[0])

# Plot the line, the points, and the nearest vectors to the plane
plt.figure(figsize=(8, 6))
plt.plot(xx, yy, 'k-', label="Decision boundary")
plt.plot(xx, yy_down, 'k--', label="Margin")
plt.plot(xx, yy_up, 'k--')

plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
            s=100, facecolors='none', edgecolors='k', label='Support vectors')
plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Greys, edgecolors='k', label='Data points')

plt.legend(prop=prop)
# plt.title("Support Vector Machine (SVM) - Linear Kernel", fontproperties=prop)
plt.xlabel("Feature 1", fontproperties=prop)
plt.ylabel("Feature 2", fontproperties=prop)
plt.grid(True, linestyle="--", linewidth=0.5)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()