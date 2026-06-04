<!--
 Copyright (c) 2026 David Such
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Hardware Version Control Log  
**Project:** Embedded AI  
**Chapter:** Chapter 14 – Battery Monitoring and Logging  

This document tracks hardware revisions for the Display and Logging Shield. Update this file whenever a schematic, PCB layout, or BOM change is made.

---

## Document Information

- **Repository:**  `https://github.com/Reefwing-Software/Embedded-AI`
- **Location:** `schematics/ch_14/`  
- **Last Updated:** 5th Jan 2026  
- **Maintained By:**  `David Such`

---

## Display and Logging Shield – Version History

### Version DLS-1.0
- **Date:** 05/08/2024  
- **Status:** Initial release  
- **Description:**  
  - First version of the display and logging shield  
  - OLED display interface  
  - SD card logging support  
  - Temperature sensor integration  

- **Schematic:** `Schematic_Display-and-Logging-Shield_2026-01-05.pdf`  
- **PCB:** `2D_pcb_display.png`  
- **Gerbers:** `Gerber_Display-and-Logging-Shield_PCB_Display-and-Logging-Shield_2026-01-05.zip`  
- **BOM:** `BOM_Display-and-Logging-Shield_2026-01-05.csv`  
- **Pick and Place:** `PickAndPlace_PCB_Display-and-Logging-Shield_2026-01-05.csv`

- **Notes:**  
  - Version used in Edition 1 of Embedded AI   

---

### Version DLS-1.1
- **Date:** YYYY-MM-DD  
- **Status:** Revision  
- **Changes:**  
  -  

- **Reason for Change:**  
- **Impact:**  
  - Electrical  
  - Mechanical  
  - Firmware  

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
