# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# Font and output paths
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_11_final")
image_name = 'f11008.pdf'
image_path = os.path.join(image_folder, image_name)

# Generate sine wave signal from -1 to 1
samples = 100
t = np.linspace(0, 2 * np.pi, samples)
signal = np.sin(t)  # Range: -1 to 1

# Simulate PDM encoding from -1 to 1 signal
pdm_output = []
integrator = 0
for s in signal:
    integrator += s
    if integrator >= 0:
        pdm_output.append(1)
        integrator -= 1
    else:
        pdm_output.append(0)
        integrator += 1

# Normalize signal to 0–1 range for plotting
normalized_signal = 0.5 * (signal + 1)

# Plotting
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.step(range(samples), pdm_output, where='mid', color='black', label='PDM output')
ax.plot(range(samples), normalized_signal, color='gray', linestyle='-', linewidth=1.5, label='Original signal (sine wave)')

ax.set_ylim(-0.2, 1.2)
ax.set_yticks([0, 0.5, 1])
ax.set_yticklabels(['0', '0.5', '1'], fontproperties=prop)
ax.set_xticks([])
ax.set_xlabel("Time", fontproperties=prop)
ax.set_title("Pulse density modulation (PDM) with original signal", fontproperties=prop)

ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.grid(True, linestyle='--', linewidth=0.5, color='grey', alpha=0.5)
ax.legend(prop=prop, loc='upper right')

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()