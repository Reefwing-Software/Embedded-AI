<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

```mermaid
graph LR
    subgraph Input Layer
        direction TB
        A1(<i>x1</i>)
        A2(<i>x2</i>)
        A3(<i>x3</i>)
        A4(<i>x4</i>)
    end
    
    subgraph Hidden Layer
        direction TB
        B1(<i>a1</i>)
        B2(<i>a2</i>)
        B3(<i>a3</i>)
    end
    
    subgraph Output Layer
        direction TB
        C1(<BR><i>y1</i><BR><BR>)
    end
    
    %% Connections
    A1 --> B1
    A1 --> B2
    A1 --> B3
    A2 --> B1
    A2 --> B2
    A2 --> B3
    A3 --> B1
    A3 --> B2
    A3 --> B3
    A4 --> B1
    A4 --> B2
    A4 --> B3
    B1 --> C1
    B2 --> C1
    B3 --> C1
    C1 --> SOC(SOC)