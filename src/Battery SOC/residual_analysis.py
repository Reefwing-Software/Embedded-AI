# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import numpy as np

# Assuming y_test and y_pred are your true and predicted SOC values

residuals = [y_test - np.clip(best_gpr_model.predict(X_test_scaled), 0, 1) for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list)]

# Flatten the lists for plotting
residuals = np.concatenate(residuals)
y_test_all = np.concatenate(y_test_list)

plt.figure(figsize=(10, 6))
plt.scatter(y_test_all, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('True SOC')
plt.ylabel('Residual (True - Predicted)')
plt.title('Residual Plot')
plt.show()

# Calculate additional metrics
mae_list = [np.mean(np.abs(y_test - np.clip(best_gpr_model.predict(X_test_scaled), 0, 1))) for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list)]
median_abs_error_list = [np.median(np.abs(y_test - np.clip(best_gpr_model.predict(X_test_scaled), 0, 1))) for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list)]

print(f'Mean Absolute Error for each temperature: {mae_list}')
print(f'Median Absolute Error for each temperature: {median_abs_error_list}')