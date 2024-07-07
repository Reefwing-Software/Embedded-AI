<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

<!--
```mermaid
graph LR
    title[Scala Naturae Brain Evolution]
    A[Ancient Life Forms] --> B[Fish]
    B --> C[Amphibians]
    C --> D[Reptiles]
    D --> E[Birds]
    E --> F[Mammals]
    F --> G[Primates]
    G --> H[Humans] 
-->

:::mermaid
graph BT
    title[Modern Approach to Brain Evolution]
    root[Ancient Life Forms] --> A[fish]
    root --> B[amphibian]
    root --> C[reptile]
    C --> D[bird]
    root --> E[mammal]
    E --> F[human]
    
    style A fill:#F9F,stroke:#333,stroke-width:2px
    style B fill:#F9F,stroke:#333,stroke-width:2px
    style C fill:#F9F,stroke:#333,stroke-width:2px
    style D fill:#F9F,stroke:#333,stroke-width:2px
    style E fill:#F9F,stroke:#333,stroke-width:2px
    style F fill:#F9F,stroke:#333,stroke-width:2px
    style root fill:#000,stroke:#000,stroke-width:4px