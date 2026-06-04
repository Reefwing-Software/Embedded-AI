<!--
 Copyright (c) 2026 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Hardware Version Control Log  
**Project:** Embedded AI - Battery Monitoring and Display Shields  
**Chapter:** Chapter 14 – Battery Monitoring and Logging  

This document tracks hardware revisions for the Battery Monitoring Shield. Update this file whenever a schematic, PCB layout, or BOM change is made.

---

## Document Information

- **Repository:**  `https://github.com/Reefwing-Software/Embedded-AI`
- **Location:** `schematics/ch_14/`  
- **Last Updated:** 5th Jan 2026  
- **Maintained By:**  `David Such`

---

## Battery Monitoring Shield – Version History

### Version BMS-1.2
- **Date:**   05/01/26
- **Status:** Built and tested  
- **Description:**  
  - Battery charge circuit  
  - Programmable discharge load  
  - Fuel gauge (BQ27441-G1A)  
  - Current sense resistor and temperature monitoring  

- **Changes:**  
  -  Added DIL switch to turn I2C pull-ups on/off

- **Reason for Change:**  I2C pull-ups can cause problems if stacking shields or using other I2C devices with pull-ups already present.
- **Impact:**  
  - Allows shield to be used solo or stacked.

- **Schematic:** `Schematic_Battery-Monitor-Shield_2026-01-04.pdf`  
- **PCB:** `2D_pcb_display.png`  
- **Gerbers:** `Gerber_Battery-Monitor-Shield_PCB_Battery-Monitor-Shield_2026-01-05.zip`  
- **BOM:** `BOM_Battery-Monitor-Shield_2026-01-05.csv`  
- **Pick and Place:** `PickAndPlace_PCB_Battery-Monitor-Shield_2026-01-05.csv`

- **Notes:**  
  - Version used in Edition 1 of Embedded AI  

---

### Version BMS-1.1
- **Date:** 06/07/2025  
- **Status:** Untested change 
- **Changes:**  
  -  Swapped polarity on battery input to match battery

- **Reason for Change:**  Removes need to swap battery lead polarity.
- **Impact:**  
  - NIL

---

### Version BMS-1.0
- **Date:** 28/10/2024  
- **Status:** Original release  

---

## Cross-Shield Compatibility

| Display Shield | Battery Shield | Status | Notes |
|---------------|---------------|--------|-------|
| DLS-1.0       | BMS-1.0       | ✅     | Fully compatible |
| DLS-1.0       | BMS-1.2       | ✅     | Fully compatible |


---

## Firmware Compatibility Notes

- Minimum firmware version:  
- Required configuration flags:  
- Known incompatibilities:  N/A

---

## Outstanding Issues / TODO



---

## Revision Log for This Document

| Date       | Author | Change Description |
|------------|--------|--------------------|
| 05/01/26   | DS     | Initial creation   |

---