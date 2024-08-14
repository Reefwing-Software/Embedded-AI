<!--
 Copyright (c) 2024 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

| Parameter                           | Symbol | Conditions           | Min   | Typ  | Max          | Unit  |
|-------------------------------------|--------|----------------------|-------|------|--------------|-------|
| Common mode input range             | Vicm1  | Low power mode       | 0.2   | -    | AVCC0 - 0.5  | V     |
|                                     | Vicm2  | High-speed mode      | 0.3   | -    | AVCC0 - 0.6  | V     |
| Output voltage range                | Vo1    | Low power mode       | 0.1   | -    | AVCC0 - 0.1  | V     |
|                                     | Vo2    | High-speed mode      | 0.1   | -    | AVCC0 - 0.1  | V     |
| Input offset voltage                | Vioff  | 3σ                   | -10   | -    | 10           | mV    |
| Open gain                           | Av     |                      | 60    | 120  | -            | dB    |
| Power supply reduction ratio        | PSRR   |                      | -     | 90   | -            | dB    |
| Common mode signal reduction ratio  | CMRR   |                      | -     | 90   | -            | dB    |
| Slew rate                           | Tslew1 | CL = 20 pF, Low power mode  | -     | 0.02 | -    | V/µs  |
|                                     | Tslew2 | High-speed mode      | -     | 1.1  | -            | V/µs  |
| Load current                        | Iload1 | Low-power mode       | -100  | -    | 100          | µA    |
|                                     | Iload2 | High-speed mode      | -100  | -    | 100          | µA    |
| Load capacitance                    | CL     |                      | -     | -    | 20           | pF    |