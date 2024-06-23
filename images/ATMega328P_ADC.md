<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

:::mermaid
graph TD
    A[Analog Input] --> B[Analog MUX]
    B --> C[Sample and Hold]
    C --> D[ADC Conversion]
    D --> E[Digital Result]
    
    B --> F[Reference Voltage]
    F --> G[Internal Vref]
    F --> H[External Aref]
    
    C --> I[Clock Source]
    I --> J[Prescaler]
    
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style E fill:#bbf,stroke:#333,stroke-width:4px
    style G fill:#bbf,stroke:#333,stroke-width:4px
    style H fill:#bbf,stroke:#333,stroke-width:4px
    style J fill:#bbf,stroke:#333,stroke-width:4px
:::

:::mermaid
graph LR
    B[Sample/hold capacitor\n14 pF\n\n] --> P
    C --> D[Logic]
    D --> E[Output]
    F[ARef] --> G[10 bit DAC]
    G --> C
    C --> G
    G --> D

    subgraph Logic
        direction LR
        
    end

    subgraph Comparator
        direction LR
        P[+]
        N[-]
    end

    subgraph MUX
        direction LR
        M0[M0]
        M1[M1]
        M2[M2]
        M3[M3]
        M4[M4]
        M5[M5]
        M6[M6]
        M7[M7]
    end
    
    subgraph Inputs
        direction LR
        AI0[A0]
        AI1[A1]
        AI2[A2]
        AI3[A3]
        AI4[A4]
        AI5[A5]
        AI6[A6]
        AI7[A7]
    end
    
    AI0 --> M0
    AI1 --> M1
    AI2 --> M2
    AI3 --> M3
    AI4 --> M4
    AI5 --> M5
    AI6 --> M6
    AI7 --> M7

    MUX --> B
    