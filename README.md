![license](https://img.shields.io/badge/license-MIT-green) ![release](https://img.shields.io/github/release-date/Reefwing-Software/Embedded-AI?color="red") ![open source](https://badgen.net/badge/open/source/blue?icon=github)

# Embedded AI — Code Repository

Welcome to the official GitHub repository for **_Embedded AI: Intelligence at the Deep Edge_**, published by **No Starch Press**.

This repository contains the source code, datasets, schematics, PCB Gerber files, and datasheets used throughout the book. Each project chapter includes practical, hands-on builds designed to help you understand and implement artificial intelligence on embedded hardware — from 8-bit microcontrollers to sensors with on-chip machine learning cores.

---

## About the Book

**_Embedded AI: Intelligence at the Deep Edge_** explores how artificial intelligence can run efficiently on small, resource-constrained devices. You'll learn how to combine embedded systems engineering with modern AI and machine learning techniques to create smart, autonomous, and connected products. The approach throughout is pragmatic and engineering-focused: practical tools, real hardware, and projects you can construct.

**Publisher:** No Starch Press, Inc.  
**Author:** David Such  
**Technical Reviewer:** John Hoffmann  
**Publication Year:** 2027 (first printing)  
**ISBN-13:** 978-1-7185-0490-5 (print)  
**ISBN-13:** 978-1-7185-0491-2 (ebook)  
**Library of Congress Control Number:** 2026020977

All hardware designs, schematics, and software developed for this book are fully open source and released under the **MIT License**, so you can modify and build upon them freely.

---

## Book Structure

The book is organised into three parts, followed by an epilogue and a resources appendix.

**Part I: Foundations of Embedded AI**
- Chapter 1: The Path to Embedded AI
- Chapter 2: The Basics of Embedded Systems
- Chapter 3: Applied Machine Learning in Embedded Projects
- Chapter 4: Deep Learning
- Chapter 5: Exploratory Data Analysis

**Part II: Working with Sensors and Data**
- Chapter 6: Smart Sensors
- Chapter 7: IMU Data Preprocessing
- Chapter 8: Sensor Fusion

**Part III: Building Complete Systems**
- Chapter 9: Sensor Machine Learning
- Chapter 10: Real-Time Audio Noise Suppression
- Chapter 11: Build an AI MIDI Synthesizer
- Chapter 12: Build a Hot Word Detection Engine
- Chapter 13: Build Arduino Battery Monitor and Logging Shields

**Epilogue:** Where Do We Go Next?  
**Resources:** Datasets, datasheets, libraries, and external links used in the book (the `data/` and `datasheets/` folders in this repository mirror many of these).

---

## Who Is This Book For?

**_Embedded AI_** is written for engineers, makers, students, and technical enthusiasts who want to bring **machine learning and artificial intelligence to the edge**.

If you're building **smart sensors, intelligent robotics, drones, or microcontroller-powered AI projects**, you're in the right place. The book aims to strike a balance between simplistic beginner guides and highly technical academic theses, explaining not just _how_ to build things, but _why_ they work the way they do.

### Intended Audience
- **Engineers and Makers** in the Arduino / Raspberry Pi community who have moved beyond beginner-level projects and want more challenging, comprehensive guides.
- **Students** in electrical engineering, computer science, robotics, or AI looking for practical projects to complement their coursework.
- **Developers** interested in learning how to optimise and deploy ML models on constrained edge devices.
- **STEM learners** who enjoy an interdisciplinary mix of statistics, cognitive theory, electronics, programming, and control systems.

### What You'll Need
You should have:
- Some understanding of **electronics and programming**
- The ability to **compile and deploy firmware** to a microcontroller
- Familiarity with **electronic schematics** (this will come in handy)

No prior machine learning experience is required. This is not a general primer on artificial intelligence: where AI concepts are introduced, they are presented to the extent required to implement working systems on resource-constrained embedded hardware.

---

## What You'll Learn

By the end of the book, you will be able to:

- **Understand the foundations of embedded AI** — Grasp the core principles of embedded systems, artificial intelligence, and how they intersect at the edge, including key industry trends, applications, and challenges.
- **Understand intelligence under constraint** — Examine how biological and artificial intelligence evolved in response to environmental and resource limits, and apply these principles to the design of practical embedded AI systems.
- **Set up your development environment** — Identify the hardware and software tools required for embedded AI development and configure your environment for project-based learning.
- **Build and analyse embedded systems** — Learn the fundamentals of embedded systems, from real-time software architectures to peripheral control, through a **signal generator** mini project.
- **Apply classical and deep machine learning techniques** — Implement supervised, unsupervised, and reinforcement learning algorithms, then transition into deep learning with **ANNs, CNNs, RNNs, and GANs**, using real-world projects like proximity detection, person detection, and music generation.
- **Perform exploratory data analysis** — Clean, visualise, and engineer features from sensor data to improve model accuracy and reliability, using **battery state of charge** as a case study.
- **Leverage smart sensors and adaptive sensing** — Understand the capabilities and limitations of modern sensors and apply techniques like **finite-state machines** and **compressed sensing** for efficient data acquisition.
- **Preprocess IMU data and perform sensor fusion** — Translate raw accelerometer, gyroscope, and magnetometer data into meaningful orientation using preprocessing, **complementary filters**, and **sensor fusion** (Madgwick, Mahony, Kalman, and on-sensor fusion).
- **Develop practical embedded AI projects** — Build and deploy real-world applications such as **audio noise suppression**, **MIDI music synthesis**, **hot word detection**, and **battery monitoring**, using platforms like **Arduino**, **Raspberry Pi Pico**, and the **Nicla** series.
- **Understand hardware–software trade-offs in embedded AI** — Balance model complexity, accuracy, and deployability by making informed design decisions that respect microcontroller constraints.
- **Envision the future of embedded AI** — Understand how embedded intelligence is evolving and explore **biologically inspired approaches** to next-generation machine learning systems.

---

## Hardware Requirements

In addition to the embedded hardware listed below, you'll need a **laptop or desktop computer** capable of running Python scripts and training machine learning models. Any modern system — **Windows**, **macOS**, or **Linux** — will work, as long as it supports **Python 3.x** and can handle basic ML training workloads.

While this book focuses on **embedded AI**, much of the **model training**, especially for deep learning, is performed on laptops, desktops, or in the cloud. Once trained, models are **quantised, compressed, and optimised** for deployment on embedded hardware. This separation of concerns — **train on the desktop, deploy at the edge** — is a pragmatic and widely adopted workflow.

Each project has a **parts list**, so you can get exactly what you need when you need it. You do not have to buy everything in advance, and you do not need most of the boards to get started:

- Around a **quarter of the chapters need no hardware at all** and can be followed entirely on a laptop with TensorFlow and scikit-learn.
- **Two-thirds of the chapters** can be completed with just two boards: the **Arduino UNO** and the **Raspberry Pi Pico** (together around $35).
- Add the **Arduino Nano 33 BLE Sense** and you can build close to **three-quarters of the projects** for a combined cost of around $70.

These three boards are reused across many projects, so they are the ones worth investing in up front. The remaining boards are each used in a single chapter. The full set of boards and platforms used across all projects is:

- Arduino UNO (R3 or R4)
- Arduino Nano 33 BLE Sense (R1 or R2)
- Arduino Nicla Vision
- Arduino Nicla Voice
- Raspberry Pi Pico (RP2040)
- Raspberry Pi Pico 2 (RP2350)
- STM32F401VE motherboard (MKI109V3) with ST ISM330BX 6-axis IMU (MKI245KA)

### Projects by Chapter

The table below lists every project in the book (matching the book's *List of Projects*), the board it targets, and the main additional components.

| # | Chapter | Project | Board / Platform | Additional Components |
|---|---------|---------|------------------|-----------------------|
| — | 2 | Bare-metal blink (Software Architectures) | Arduino UNO R3 | — |
| 1 | 2 | Build a Signal Generator | Raspberry Pi Pico (RP2040) | Makerverse 10-bit R-2R DAC (MCP6001 buffer), breadboard, oscilloscope (recommended) |
| 2 | 3 | Using a Lookup Table to Monitor Battery SOC | Arduino UNO R3 | 3S LiPo battery, voltage divider, breadboard |
| 3 | 3 | Using Machine Learning to Monitor Battery SOC | Arduino UNO R3 | 3S LiPo battery, breadboard (model trained on the LG 18650HG2 dataset) |
| 4 | 4 | Detect Proximity Using ANNs | Arduino Nano 33 BLE Sense Rev 2 | — (on-board APDS9960) |
| 5 | 4 | Detect People Using CNNs | Arduino Nicla Vision | — (on-board GC2145 camera) |
| 6 | 4 | Generate Music with GAN | Software only | — |
| 7 | 5 | EDA for Battery SOC Prediction | Software only | — |
| 8 | 6 | Using Compressed Sensing for Efficient Sampling | Arduino UNO R3 / R4 | DHT11 temperature/humidity sensor, 5.1 kΩ pull-up, breadboard |
| 9 | 6 | Program an FSM to Detect Position | ST ISM330BX (MKI245KA) | MKI109V3 motherboard, DIL24 adapter (MKIGI06A) |
| 10 | 7 | Testing Accelerometer Angle Formulas | Arduino Nano 33 BLE Rev 1 | Breadboard, digital angle gauge (Klein Tools 935DAG) |
| 11 | 8 | Estimate Orientation with a Complementary Filter | Arduino Nano 33 BLE Sense Rev 2 | — (on-board BMI270 / BMM150) |
| 12 | 8 | Compare Sensor Fusion Filters | Arduino Nano 33 BLE Sense Rev 1 | — (synthetic IMU data) |
| 13 | 8 | Measure the Static Angle Accuracy of IMUs | Arduino Nano 33 BLE Sense Rev 1 | Nano 33 BLE Sense Rev 2, Arduino Nano v3 + MPU6050 (GY-521), digital angle gauge |
| 14 | 8 | Test Embedded Sensor Fusion on the ISM330BX | ST ISM330BX (MKI245KA) | MKI109V3 motherboard |
| 15 | 9 | Detect Faults in a Robot Arm | Arduino UNO | 6-DOF robot arm (MG996R servos), Pololu Maestro 6-channel servo controller, 5 V 15 A power supply (Mean Well LRS-75-5), ST ISM330BX + MKI109V3 |
| 16 | 10 | Benchmarking the Pico and Pico 2 | Raspberry Pi Pico / Pico 2 | — |
| 17 | 10 | Real-Time Audio Noise Suppression | Raspberry Pi Pico 2 (RP2350) | Reefwing Noise Suppression carrier PCB, TDK T3902 PDM microphone, DFRobot DFR0664 2.0" LCD |
| 18 | 11 | Software Toolchain Testing | Raspberry Pi Pico (RP2040) | — |
| 19 | 11 | Model Quantization | Software only | — |
| 20 | 11 | GAN Deployment Testing | Raspberry Pi Pico (RP2040) | — |
| 21 | 11 | Piano Keyboard and Control Building | Raspberry Pi Pico (RP2040) | Reefwing Pico MIDI Keyboard PCB (capacitive touch) |
| 22 | 11 | Build the Hardware Synthesizer | VS1053b | Reefwing MIDI Synthesizer PCB (VS1053b, AP7312 LDO, 6N138-L optocoupler) |
| 23 | 11 | Keyboard Controller to USB MIDI Device Conversion | Raspberry Pi Pico (RP2040) | Pico MIDI Keyboard PCB |
| 24 | 11 | Add AI Music Generation to the MIDI Controller | Raspberry Pi Pico (RP2040) | Pico MIDI Keyboard PCB, MIDI Synthesizer PCB |
| 25 | 11 | Add Procedural Composition to the MIDI Controller | Raspberry Pi Pico (RP2040) | Pico MIDI Keyboard PCB, MIDI Synthesizer PCB |
| 26 | 12 | Verify the Nicla Voice and Toolchain | Arduino Nicla Voice | — |
| 27 | 12 | Train a Custom Hot Word Model | Arduino Nicla Voice | — |
| 28 | 12 | Improve Model Performance | Arduino Nicla Voice | — |
| 29 | 12 | Deploy a Hot Word Model and Test It | Arduino Nicla Voice | — |
| 30 | 13 | Build a DC Load Prototype | Arduino UNO R4 Minima | Breadboard, STP60NF06 MOSFET + heatsink, op-amp voltage follower (on-chip) |
| 31 | 13 | Build and Test the Display and Logging Shield | Arduino UNO R4 Minima | Reefwing Display & Logging Shield, DFRobot DFR0650 0.96" OLED, Adafruit microSD breakout, DHT11 |
| 32 | 13 | Build and Test the Battery Monitoring Shield | Arduino UNO R4 Minima | Reefwing Battery Monitor Shield (BQ24075 charger, BQ27441 fuel gauge, programmable load), 1100 mAh 603450 LiPo |

Chapter 13 concludes by testing the complete stack (UNO R4 + both shields) through full charge, discharge, and cycle tests logged to SD card.

### Custom PCBs

Five projects use **custom Reefwing PCBs**, which you'll need to **fabricate and assemble** before use. Schematics, bills of materials, and **Gerber files** are in the `schematics/` folder and can be uploaded directly to your preferred PCB manufacturer. Allow **1–2 weeks** for fabrication and shipping, depending on your supplier and location.

| Chapter | PCB | Folder |
|---------|-----|--------|
| 10 | Noise Suppression carrier board (Pico 2 + T3902 + DFR0664) | `schematics/ch_10/` |
| 11 | Pico MIDI Keyboard (capacitive touch, v1 and v2) | `schematics/ch_11/Pico Keyboard/`, `schematics/ch_11/Pico Keyboard v2/` |
| 11 | MIDI Synthesizer (VS1053b) | `schematics/ch_11/MIDI Synthesizer/` |
| 13 | Display and Logging Shield | `schematics/ch_13/Display and Logging Shield/` |
| 13 | Battery Monitor Shield | `schematics/ch_13/Battery Monitor Shield/` |

### Tools for Assembly and Debugging

A basic maker's toolbox is enough: screwdrivers, long-nosed pliers, wire cutters, and jumper wires, plus a soldering iron if you assemble your own PCBs. For debugging, a **multimeter** is the one tool to have; an **oscilloscope** is very useful for the signal generator project. A logic analyser, LCR meter, and JTAG/SWD debugger are helpful but not essential.

---

## Software Requirements

A diverse set of software tools is needed to complete the projects. They span the full stack of embedded AI development, from compiling C/C++ firmware to training neural networks in Python and deploying models with TensorFlow Lite for Microcontrollers. The primary requirements, as listed in the book's introduction, are:

- **Languages and runtimes:** Python, C/C++
- **IDEs and editors:** Arduino IDE, VS Code (with the Pico SDK extension for Chapters 10 and 11), OpenMV IDE, MEMS-Studio
- **Toolchains and build tools:** AVR-GCC and AVRDUDE, Make, Arduino CLI, Pico SDK
- **Frameworks:** TensorFlow Lite for Microcontrollers, Edge Impulse, RNNoise, CMSIS-DSP
- **Utilities:** CoolTerm, Audacity, FluidSynth, TensorBoard, Netron, xxd, Syntiant Uploader

The table below breaks the requirements down by chapter and project.

| Chapter | Section / Project | Software |
|---------|-------------------|----------|
| 2 | Software Architectures (super loop, bare metal) | Arduino IDE; Terminal, text editor, AVR-GCC, AVRDUDE, Make |
| 2 | Build a Signal Generator | VS Code, Pico SDK, CMake |
| 3 | Linear Regression | Python, VS Code, NumPy, pandas, matplotlib |
| 3 | Using a Lookup Table to Monitor Battery SOC | Arduino IDE |
| 3 | Using Machine Learning to Monitor Battery SOC | Python, VS Code, scikit-learn, scipy, joblib |
| 4 | Detect Proximity Using ANNs | Python, TensorFlow, VS Code, xxd, TensorFlow Lite for Microcontrollers, Arduino IDE |
| 4 | Detect People Using CNNs | OpenMV IDE, Arduino IDE, TensorFlow Lite for Microcontrollers, Python, VS Code |
| 4 | Generate Music with GAN | Python, TensorFlow, VS Code, music21, FluidSynth, pyFluidSynth, midi2audio |
| 5 | EDA for Battery SOC Prediction | Python, VS Code, pandas, NumPy, matplotlib, seaborn, scipy, scikit-learn |
| 6 | Using Compressed Sensing for Efficient Sampling | Arduino IDE, DHT11 library, Python (NumPy, matplotlib, scipy, statsmodels, CVXPY) |
| 6 | Program an FSM to Detect Position | MEMS-Studio |
| 7 | Testing Accelerometer Angle Formulas | Arduino IDE, Reefwing LSM9DS1 library |
| 8 | Complementary filter, filter comparison, static angle testing | Arduino IDE, Reefwing AHRS and Reefwing IMU Types libraries, CoolTerm, Python |
| 8 | Test Embedded Sensor Fusion on the ISM330BX | MEMS-Studio |
| 9 | Detect Faults in a Robot Arm | Arduino IDE, PololuMaestro and AltSoftSerial libraries, Pololu Maestro Control Center, MEMS-Studio |
| 10 | Benchmarking the Pico and Pico 2 | VS Code with Pico SDK extension, CMake, RNNoise |
| 10 | Real-Time Audio Noise Suppression | VS Code with Pico SDK extension, CMake, RNNoise, microphone-library-for-pico, TinyUSB, CMSIS-DSP / CMSIS 6, Reefwing ST7789 library, Audacity, CoolTerm (or other serial terminal), EasyEDA (PCB) |
| 11 | Build an AI MIDI Synthesizer (Projects 18–25) | VS Code with Pico SDK extension, CMake, pioasm, Python, TensorFlow / TensorFlow Lite (quantisation), pico-tflmicro (TensorFlow Lite for Microcontrollers), xxd, TinyUSB, FluidSynth with the FluidR3_GM soundfont, MIDI View, EasyEDA (PCB) |
| 12 | Build a Hot Word Detection Engine (Projects 26–29) | Arduino IDE, Arduino CLI, Edge Impulse Studio and CLI (Node.js / npm), Syntiant Uploader, Netron, Python (pyserial) |
| 13 | Build Arduino Battery Monitor and Logging Shields (Projects 30–32) | Arduino IDE, U8g2 display library, Arduino SD library, SparkFun BQ27441 library, CoolTerm, Python |

We've aimed to select tools that are **open source**, **widely available**, and **cross-platform**, compatible with **Windows**, **macOS**, and **Linux**. While we recommend tools like **Visual Studio Code**, **Terminal**, and specific **Python libraries**, feel free to substitute your preferred equivalents. Download links for all referenced software are in the book's **Resources** appendix.

**Windows on Arm note:** at the time of writing, Windows Arm-based systems have issues with driver-dependent or emulated tools, which affects the Arduino IDE (DFU drivers), AVR-GCC, AVRDUDE, FluidSynth, Audacity, MEMS-Studio, CoolTerm, and OpenMV IDE. Native Arm64 Python builds also lack some required libraries (notably pandas); the workaround is to install the standard x86 build of Python and run it under emulation.

---

## Getting Help

If you spot an error, have a question, or want to share an alternate method, **we welcome your input**. Collaboration and continuous improvement are central to the open source spirit of this book.

The best place to **report issues**, **suggest enhancements**, or **ask questions** is through this GitHub repository:

**Repository:** [Embedded AI](https://github.com/Reefwing-Software/Embedded-AI)

There you'll find:
- An **issue tracker** for reporting typos, bugs, or errors
- A **discussion forum** for sharing insights, ideas, or improvements
- Direct access to all **source code and examples**

Whether it's a typo, a bug, or a clever optimisation you'd like to share, we'd love to hear from you.

---

## Repository Structure

The repository is organised by chapter (`ch_N/`) within each top-level folder. Source folders and files named `cNNMMM` (for example `src/ch_4/c04003`) correspond to the numbered code listings in the book; other folders are named after the project they belong to.

```text
📂 Embedded-AI/
├── LICENSE                     MIT License
├── README.md
├── data/                       Datasets and captured results used by the projects
│   ├── ch_3/                   LG 18650HG2 battery dataset, capacity tables
│   ├── ch_4/                   Proximity (near-ear) training data
│   ├── ch_5/                   Preprocessed / train / test splits for EDA
│   ├── ch_6/                   Compressed sensing sensor data
│   ├── ch_7/                   Accelerometer angle results
│   ├── ch_8/                   Filter test and static angle results (LSM9DS1, BMI270, MPU6050, ISM330BX)
│   ├── ch_10/                  CMU Arctic speech samples, clean / noisy audio
│   ├── ch_11/                  GAN generator models (.tflite) and Pico inference output
│   ├── ch_12/                  Edge Impulse keyword dataset and exported models
│   └── ch_13/                  Battery charge / discharge / cycle logs
├── datasheets/                 Datasheets, application notes, and reference papers by chapter
│   ├── ch_1/  ch_2/  ch_4/  ch_6/  ch_7/  ch_8/  ch_9/  ch_10/  ch_11/  ch_13/
├── ndp120/                     Syntiant NDP120 firmware packages and uploader binaries (Chapter 12)
├── schematics/                 Schematics, BOMs, PCB layouts, and Gerber files
│   ├── ch_3/                   Battery SOC monitor schematic
│   ├── ch_10/                  Noise Suppression carrier PCB
│   ├── ch_11/                  MIDI Synthesizer, Pico Keyboard, Pico Keyboard v2
│   └── ch_13/                  Battery Monitor Shield, Display and Logging Shield, breadboard prototypes
├── soundfonts/
│   └── FluidR3_GM/             General MIDI soundfont for FluidSynth (Chapters 4 and 11)
└── src/                        Source code by chapter
    ├── ch_1/                   Figures only (no code)
    ├── ch_2/                   bare-metal-blink, pico-awg, pico-awg-dma, pico-dma-irq
    ├── ch_3/                   Lookup table sketch, GPR training and evaluation scripts
    ├── ch_4/                   ANN proximity, person_detection, GAN music generation
    ├── ch_5/                   EDA scripts
    ├── ch_6/                   Compressed sensing sketch
    ├── ch_7/                   Accelerometer angle sketches, gyro_test
    ├── ch_8/                   classic_complementary_filter, filter_test, static_angle_* sketches
    ├── ch_9/                   Robot arm control and data collection sketches
    ├── ch_10/                  pdm-microphone, pico-rnn-benchmark, pico2-rnn-benchmark,
    │                           pico2-usb-microphone, pico2-audio-spectrogram, st7789_lcd
    ├── ch_11/                  blink, generator_test, pico-keyboard(-2), pico-usb-midi, pico-ai,
    │                           pico-composition, pico-tflmicro, quantisation scripts
    ├── ch_12/                  AlexaDemo, Nicla Voice firmware, hello-world Syntiant library,
    │                           synthetic keyword generator
    └── ch_13/                  dac_test, dc_load, display_tester, sd_card_tester,
                                battery_shield_tester, battery_*_tester, battery_logger
```

Most `src/ch_N/` folders also contain an `images/` subfolder with the figures for that chapter.
