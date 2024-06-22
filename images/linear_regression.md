<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

```mermaid
graph TD
    A[Linear Regression]
    A --> B((1, 2))
    A --> C((2, 4))
    A --> D((3, 5))
    A --> E((4, 4.5))
    A --> F((5, 7))
    B --> |Line of Best Fit| G[(y = 1.2x + 0.8)]
    C --> G
    D --> G
    E --> G
    F --> G
