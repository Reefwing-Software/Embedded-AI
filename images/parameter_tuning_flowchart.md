<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

```mermaid
graph TD
     %%{ init: { 'flowchart': { 'curve': 'linear' } } }%%
    A[Parameters] --> B[Cross-validation]
    B --> C[Best parameters]
    C --> D[Retrained model]
    D --> E[Final evaluation]
    F[Dataset] --> G[Training data]
    G ~~~ H
    F --> H[Test data]
    G --> B
    G --> D
    H --> E