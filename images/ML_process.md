<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

:::mermaid
flowchart LR
    subgraph Machine Learning Process
        direction LR
        subgraph Engineering
            direction TB
            A(Define the Problem) --> B(Collect & Clean Data)
            B --> C(Select a Model)
            C --> D(Train the Model)
        end

        subgraph Evaluation
            direction TB
            F(Evaluate the Model)
            F --> G(Tune the Model)
            G --> H(Deploy the Model)
            H --> I(Monitor and Maintain) 
        end
    end
    Engineering --> Evaluation
:::
