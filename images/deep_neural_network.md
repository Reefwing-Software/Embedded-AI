<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

```mermaid
graph LR
    subgraph InputLayer["Input Layer"]
        direction TB
        A1["<i>x1</i>"]
        A2["<i>x2</i>"]
        A3["<i>x3</i>"]
    end
    
    subgraph HiddenLayer1["Hidden Layer 1"]
        direction TB
        B1["a1"]
        B2["a2"]
        B3["a3"]
    end
    
    subgraph HiddenLayer2["Hidden Layer 2"]
        direction TB
        C1["b1"]
        C2["b2"]
        C3["b3"]
    end
    
    subgraph HiddenLayer3["Hidden Layer 3"]
        direction TB
        D1["c1"]
        D2["c2"]
        D3["c3"]
    end
    
    subgraph OutputLayer["Output Layer"]
        direction TB
        E1["SOC"]
    end
    
    %% Connections from Input to Hidden Layer 1
    A1 --> B1
    A1 --> B2
    A1 --> B3
    A2 --> B1
    A2 --> B2
    A2 --> B3
    A3 --> B1
    A3 --> B2
    A3 --> B3
    
    %% Connections from Hidden Layer 1 to Hidden Layer 2
    B1 --> C1
    B1 --> C2
    B1 --> C3
    B2 --> C1
    B2 --> C2
    B2 --> C3
    B3 --> C1
    B3 --> C2
    B3 --> C3
    
    %% Connections from Hidden Layer 2 to Hidden Layer 3
    C1 --> D1
    C1 --> D2
    C1 --> D3
    C2 --> D1
    C2 --> D2
    C2 --> D3
    C3 --> D1
    C3 --> D2
    C3 --> D3
    
    %% Connections from Hidden Layer 3 to Output Layer
    D1 --> E1
    D2 --> E1
    D3 --> E1