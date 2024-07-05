<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Summary of Hyperparameter Tuning Trials 1 - 2

| Trial Number | Constant Kernel Value (\(C\)) | RBF Length Scale (\(l\)) | Best Cross-Validation Score (\( R^2 \)) | Total Script Execution Time (minutes:seconds) | Notes                                        |
|--------------|-------------------------------|--------------------------|----------------------------------------|-----------------------------------------------|----------------------------------------------|
| 1            | 0.01                          | 0.5                      | -1102.22                               | 15:33.09                                      | Initial configuration                         |
| 2            | 0.423401                      | 0.00249                  | -1.75                                  | 344:46.89                                     | Increased the upper bound for constant_value from 0.1 to 1.0. Decreased the lower bound for length_scale from 0.01 to 0.001. |

# Summary of Hyperparameter Tuning Trials 1 - 3

| Trial Number | Initial Constant (\(C\)) | Optimized Constant (\(C\)) | Constant Bounds      | Initial Length (\(l\)) | Optimized Length (\(l\)) | RBF Bounds     | Best Cross-Validation Score (\( R^2 \)) | Execution Time (minutes:seconds)                       | Notes                                        |
|--------------|---------------------------|----------------------------|----------------------|------------------------|--------------------------|----------------|----------------------------------------|-----------------------------------------------|----------------------------------------------|
| 1            | 0.01                      | 0.01                       | (0.001, 0.1)         | 0.5                    | 0.5                      | (0.01, 1.0)    | -1102.22                               | 15:33.09                                      | Initial configuration                         |
| 2            | 0.01                      | 0.423401                   | (0.1, 1.0)           | 0.25                   | 0.00249                  | (0.001, 0.1)   | -1.75                                  | 344:46.89                                     | Adjusted Constant and RBF bounds. |
| 3            | 0.4                       | 0.423401                   | (0.1, 1.0)           | 0.001                  | 0.00249                  | (0.001, 0.1)   | -1.75                                  | 356:44.66                                     | Increased max_iter, initial values and adjusted bounds.        |