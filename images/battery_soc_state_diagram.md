<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

:::mermaid
flowchart TB
     %%{ init: { 'flowchart': { 'curve': 'linear' } } }%%
    A[Initial State] --> B[Standby State]
    A --> C[Charge State]
    A --> D[Discharge State]
    B --> E[Transitional State]
    B --> C
    C --> D
    C --> B
    D --> E
    D --> B
    E --> B
    E --> D