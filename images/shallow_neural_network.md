<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

'''mermaid
graph LR
    %%{ init: { 'flowchart': { 'curve': 'linear' } } }%%
    %% Input Layer
    A1(Input 1)
    A2(Input 2)
    A3(Input 3)
    A4(Input 4)
    
    %% Hidden Layer
    B1(Hidden 1)
    B2(Hidden 2)
    B3(Hidden 3)
    
    %% Output Layer
    C1(Output)
    
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