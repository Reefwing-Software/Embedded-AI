<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Summary of Hyperparameter Tuning Trials

| Trial Number | Constant Kernel Value (\(C\)) | RBF Length Scale (\(l\)) | Best Cross-Validation Score (\( R^2 \)) | Total Script Execution Time (minutes:seconds) | Notes                                        |
|--------------|-------------------------------|--------------------------|----------------------------------------|-----------------------------------------------|----------------------------------------------|
| 1            | 0.01                          | 0.5                      | -1102.22                               | 15:33.09                                      | Initial configuration                         |
| 2            | 0.423401                      | 0.00249                  | -1.75                                  | 344:46.89                                     | Increased the upper bound for constant_value from 0.1 to 1.0. Decreased the lower bound for length_scale from 0.01 to 0.001. |