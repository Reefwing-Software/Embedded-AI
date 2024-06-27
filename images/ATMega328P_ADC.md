<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

```mermaid
graph TB
    %%{ init: { 'flowchart': { 'curve': 'linear' } } }%%
    AI0 --> M0
    AI1 --> M1
    AI2 --> M2
    AI3 --> M3
    AI4 --> M4
    AI5 --> M5
    AI6 --> M6
    AI7 --> M7

    MUX --> B

    B(Sample/hold capacitor\n14 pF\n\n) --> P
    O --> Lin
    Lout --> R(Result)
    Dref --- Aref[Aref]

    subgraph Analysis
        ADC(ADC)

        subgraph Comparator
            direction TB
            P[+]
            N[-]
            O[O/P]
        end

        subgraph Conversion
            Lfb --> Dfb
            DACout --> N

            subgraph DAC
                direction LR

                subgraph Dout
                    DACout[DACout]
                end

                subgraph Din
                    Dref[Dref]
                    Dfb[Dfb]
                end
            end

            subgraph Logic
                direction TB

                subgraph LIN
                    Lin[Lin]
                end

                subgraph LOUT
                    Lout[Lout]
                    Lfb[Lfb]
                end

            end

        end

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
    
    subgraph IO
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