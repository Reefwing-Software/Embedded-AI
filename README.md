![license](https://img.shields.io/badge/license-MIT-green) ![release](https://img.shields.io/github/release-date/Reefwing-Software/Embedded-AI?color="red") ![open source](https://badgen.net/badge/open/source/blue?icon=github)

# Embedded AI — Code Repository

Welcome to the official GitHub repository for **_Embedded AI: Intelligence at the Deep Edge_**, published by **No Starch Press**.

This repository contains all of the source code, data files, and project examples used throughout the book. Each chapter includes practical, hands-on projects designed to help you understand and implement artificial intelligence on embedded hardware platforms — from simple microcontrollers to advanced edge processors.

---

## About the Book

**_Embedded AI: Intelligence at the Deep Edge_** explores how artificial intelligence can run efficiently on small, resource-constrained devices. You’ll learn how to combine embedded systems engineering with modern AI and machine learning techniques to create smart, autonomous, and connected products.

**Publisher:** No Starch Press  
**Author:** David Such  
**Publication Date:** 2025  
**ISBN:** _TBA_

---

## Who is This Book For?

**_Embedded AI: Intelligence at the Deep Edge_** is written for engineers, makers, students, and technical enthusiasts who want to bring **machine learning and artificial intelligence to embedded systems**.  

If you're building **smart sensors, intelligent robots, drones, or microcontroller-powered AI projects**, this book will guide you through both the theory and the practice. It strikes a balance between **hands-on engineering** and **conceptual understanding**, explaining not just _how_ to build things, but _why_ they work the way they do.

### Intended Audience
- **Engineers and Makers** expanding from basic Arduino or Raspberry Pi projects into AI-powered systems.  
- **Students** in electrical engineering, computer science, robotics, or AI looking for practical projects to complement their coursework.  
- **Developers** interested in learning how to optimize and deploy ML models on constrained edge devices.  
- **Educators and STEM enthusiasts** exploring an interdisciplinary mix of electronics, programming, control systems, and cognitive theory.

### What You’ll Need
You should have:
- Basic understanding of **electronics and programming**  
- Ability to **compile and upload firmware** to a microcontroller  
- Familiarity with **electronic schematics**

No prior machine learning experience is required — this book will guide you from first principles to working AI applications on real hardware.

This book is for those who learn best by **doing**, combining **conceptual depth** with **real-world projects** that bridge the gap between theory and practice.

---

## What You’ll Learn

This book is designed to equip you with the **knowledge and hands-on experience** needed to design, develop, and deploy intelligent systems at the edge. By the end of this book, you will be able to:

- **Understand the foundations of embedded AI** — Grasp the core principles of embedded systems, artificial intelligence, and how they intersect at the edge, including key industry trends, applications, and challenges.  
- **Explore the evolution of intelligence** — Trace the development of biological and artificial intelligence and understand the **Primal Layers** framework for building embodied intelligence.  
- **Set up your development environment** — Identify the hardware and software tools required for embedded AI development and configure your environment for project-based learning.  
- **Build and analyze embedded systems** — Learn the fundamentals of embedded architectures, peripheral control, and real-time software design through a **signal generator mini project**.  
- **Apply classical and deep machine learning techniques** — Implement supervised, unsupervised, and reinforcement learning algorithms, then transition into deep learning with **ANNs, CNNs, RNNs, and GANs**, using real-world projects like proximity detection, person detection, and music generation.  
- **Perform exploratory data analysis** — Clean, visualize, and engineer features from sensor data to improve model accuracy and reliability, using **battery state-of-charge** as a case study.  
- **Leverage smart sensors and adaptive sensing** — Understand the capabilities and limitations of modern sensors and apply techniques like **Finite State Machines** and **compressed sensing** for efficient data acquisition.  
- **Preprocess IMU data and perform sensor fusion** — Translate raw accelerometer, gyroscope, and magnetometer data into meaningful orientation using preprocessing, **complementary filters**, and **sensor fusion**.  
- **Develop practical embedded AI projects** — Build and deploy real-world applications such as **audio noise suppression**, **MIDI music synthesis**, **hot word detection**, and **battery monitoring**, using platforms like **Arduino**, **Raspberry Pi**, and **Nicla** boards.  
- **Understand hardware–software trade-offs in embedded AI** — Balance model complexity, accuracy, and deployability by making informed design decisions that respect microcontroller constraints.  
- **Envision the future of embedded AI** — Explore how embedded intelligence is evolving and discover **biologically inspired approaches** to next-generation machine learning systems.

---

## Hardware Requirements

In addition to the embedded hardware listed below, you’ll need a **laptop or desktop computer** capable of running Python scripts and training machine learning models. Any modern system — **Windows**, **macOS**, or **Linux** — will work, as long as it supports **Python 3.x** and can handle basic machine learning workloads.

While this book focuses on **embedded AI**, most **model training**, particularly for deep learning, is performed on **laptops, desktops, or in the cloud**. These environments provide the **processing power and memory** required to manage large datasets and complex computations that would be impractical on microcontrollers.

Once models are trained, they are **quantized, compressed, and optimized** for deployment on embedded targets. This approach — **train on the desktop, deploy at the edge** — is the standard and most practical workflow for embedded AI development.

Each project chapter includes a detailed **Bill of Materials (BOM)**, listing the exact components required.

The Table below summarizes the **primary hardware platforms** used across all chapters. You’ll find that some boards are reused — particularly the **Arduino UNO R3 and R4 Minima**, **Arduino Nano 33 BLE Sense**, and **Raspberry Pi Pico/Pico 2** — making them smart early investments.

| Chapter | Section / Project                               | Board / Platform                                   | Additional Components                                                                                                      |
|----------|--------------------------------------------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| 3        | Super Loops                                     | Arduino UNO R3                                     | —                                                                                                                          |
| 3        | Project: Building a Signal Generator            | Raspberry Pi Pico (RP2040)                         | Makerverse 10-bit R-2R DAC, Breadboard                                                                                     |
| 4        | Project: SOC with Lookup Table                  | Arduino UNO R3                                     | 3S LiPo Battery, Breadboard                                                                                                |
| 4        | Project: SOC with Machine Learning              | Arduino UNO R3                                     | 3S LiPo Battery, Breadboard                                                                                                |
| 5        | Project: Proximity Detection using ANNs         | Arduino Nano 33 BLE Sense Rev 2                    | —                                                                                                                          |
| 5        | Project: Person Detection using CNN             | Arduino Nicla Vision                               | —                                                                                                                          |
| 7        | Project: Compressed Sensing                     | Arduino UNO R3                                     | DHT11 Temperature Sensor                                                                                                   |
| 7        | Project: Sensor Orientation using FSM           | ST ISM330BX 6-axis IMU (MKI245KA)                  | STM32F401VE Motherboard (MKI109V3)                                                                                        |
| 8        | Converting G-force to an Angle                  | Arduino Nano 33 BLE Sense Rev 1                    | —                                                                                                                          |
| 8        | Project: Comparing Accelerometer Formulas       | Arduino Nano 33 BLE Sense Rev 1                    | Breadboard                                                                                                                 |
| 9        | Sensor Fusion                                   | Arduino Nano 33 BLE Sense Rev 2                    | —                                                                                                                          |
| 9        | Project: Filter Testing                         | Arduino Nano 33 BLE Sense Rev 1                    | MPU6050 IMU (GY-521), Breadboard, Arduino Nano v3                                                                          |
| 9        | Embedded Sensor Fusion                          | STM32F401VE Motherboard (MKI109V3)                 | ST ISM330BX 6-axis IMU (MKI245KA)                                                                                         |
| 10       | Sensor Machine Learning                         | STM32F401VE Motherboard (MKI109V3)                 | ST ISM330BX 6-axis IMU (MKI245KA)                                                                                         |
| 10       | Project: Robot Arm Anomaly Detection            | Arduino UNO R3                                     | 6-DOF robot arm, Pololu Maestro 6-channel servo controller, 5 V 15 A regulated power supply                                |
| 11       | Project: Real-time Audio Noise Suppression      | Raspberry Pi Pico 2 (RP2350)                       | DFRobot DFR0664 2.0” LCD, Reefwing Noise Suppression carrier board                                                         |
| 12       | Project: AI MIDI Synthesizer                    | Raspberry Pi Pico (RP2040)                         | Reefwing Pico MIDI Keyboard PCB, Reefwing VS1053 Synthesizer PCB                                                           |
| 13       | Project: Hot Word Detection                     | Arduino Nicla Voice                                | —                                                                                                                          |
| 14       | Project: Battery Monitor and Logging            | Arduino UNO R4 Minima                              | 1100 mAh LiPo Battery, Reefwing Battery Monitor Shield, Reefwing Display & Logging Shield, 0.96” OLED, microSD Breakout    |

You don’t need to purchase all components in advance. Review the table, decide which projects you’d like to build first, and assemble the necessary hardware as you go.

Some projects use **custom Reefwing PCBs**, which you’ll need to **fabricate and assemble** before use. The repository includes **Gerber files** that you can upload directly to your preferred PCB manufacturer.

Allow **1–2 weeks** for fabrication and shipping, depending on your supplier and location.

---

## Software Requirements

A diverse set of software tools is required to complete the projects in this book. The table below summarizes the primary software requirements, organized by chapter and project.

| Chapter | Section                                                       | Software                                                                                                                                                                                                 |
|----------|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 3        | Super Loops                                                   | Arduino IDE                                                                                                                                                                                              |
| 3        | Compiling, Uploading, and Running a Bare-metal Program        | Terminal, Text Editor, AVR-GCC, AVR-DUDE, Make                                                                                                                                                           |
| 3        | Project: Building a Signal Generator                          | VS Code                                                                                                                                                                                                  |
| 4        | Linear Regression                                             | Python, VS Code                                                                                                                                                                                          |
| 4        | Project: Monitoring Battery State of Charge using a Lookup Table | Arduino IDE                                                                                                                                                                                              |
| 4        | Project: Monitoring Battery State of Charge using Machine Learning | Python, VS Code, Scikit-learn                                                                                                                                                                            |
| 5        | Artificial Neural Networks                                    | Python, VS Code                                                                                                                                                                                          |
| 5        | Project: Proximity Detection using ANNs                       | Arduino IDE, Python, VS Code, xxd, TensorFlow Lite for Microcontrollers                                                                                                                                  |
| 5        | Project: Person Detection using CNN                           | TensorFlow Lite for Microcontrollers, OpenMV IDE, Python, VS Code, Arduino IDE                                                                                                                           |
| 5        | Project: Music Generation using an LSTM RNN                   | Python, VS Code, FluidSynth, pyFluidSynth, Mido, TensorBoard                                                                                                                                             |
| 5        | Project: Music Generation using a GAN                         | Python, VS Code, music21                                                                                                                                                                                 |
| 5        | Training Locally Versus in the Cloud                          | Colab                                                                                                                                                                                                    |
| 6        | EDA                                                           | Python, VS Code, pandas, Scikit-learn                                                                                                                                                                    |
| 7        | Project: Compressed Sensing                                   | Arduino IDE, Python, VS Code                                                                                                                                                                             |
| 7        | Project: Sensor Orientation Using FSM                         | MEMS Studio                                                                                                                                                                                              |
| 8        | Converting G-force to an Angle                                | Arduino IDE, Reefwing LSM9DS1 IMU Library                                                                                                                                                                |
| 9        | Sensor Fusion                                                 | Arduino IDE, Reefwing AHRS and IMU types Library                                                                                                                                                         |
| 9        | Project: Filter Testing                                       | Arduino IDE, CoolTerm                                                                                                                                                                                    |
| 9        | Embedded Sensor Fusion                                        | MEMS Studio                                                                                                                                                                                              |
| 10       | Sensor Machine Learning                                       | Arduino IDE, MEMS Studio                                                                                                                                                                                 |
| 11       | Project: Real-time Audio Noise Suppression                    | RNNoise, VS Code, Pico SDK extension for VS Code, Make, Arm Microphone Library for Pico, Audacity, Reefwing ST7789 Library for Pico 2, CMSIS-Core, CMSIS-DSP, Terminal                                   |
| 12       | Project: An AI MIDI Synthesizer                               | VS Code, Pico SDK extension for VS Code, TensorFlow Lite for Microcontrollers, xxd, Terminal, FluidSynth, Python, TinyUSB, Midi View                                                                    |
| 13       | Project: Hot Word Detection                                   | Arduino IDE, Edge Impulse, Syntiant Uploader, Arduino CLI, Edge Impulse audio firmware, Netron                                                                                                           |
| 14       | Project: Battery Monitor and Logging                          | Arduino IDE, U8g2 Display Library, CoolTerm, Python                                                                                                                                                      |

These tools cover the full spectrum of **embedded AI development**, from compiling firmware to training and deploying machine learning models:

- **Embedded development** — Compile and upload C++ firmware using the **Arduino IDE** or **PlatformIO**.  
- **Model training** — Use **Python** and **VS Code** to train and test neural networks.  
- **Deployment** — Optimize and deploy trained models with **TensorFlow Lite for Microcontrollers**.  
- **Data capture and visualization** — Collect and analyze sensor data using **terminal utilities**, **serial monitors**, and **Python notebooks**.

We’ve selected tools that are **open-source**, **widely available**, and **cross-platform**, ensuring compatibility with **Windows**, **macOS**, and **Linux** environments.  
While we recommend industry-standard options like **Visual Studio Code**, **Arduino IDE**, and common **Python libraries**, you’re encouraged to substitute your preferred equivalents.

Download links and setup instructions for all required tools can be found in **Appendix A: Book Resources**.

---

## Getting Help

If you spot an error, have a question, or want to share an alternate method, **we welcome your input**. Collaboration and continuous improvement are at the heart of the open-source spirit behind this book.

The best place to **report issues**, **suggest enhancements**, or **ask questions** is through this GitHub repository:

**Repository:** [Embeddded AI](https://github.com/Reefwing-Software/Embedded-AI)

There you’ll find:
- An **issue tracker** for reporting typos, bugs, or errors  
- A **discussion forum** for sharing insights, ideas, or improvements  
- Direct access to all **source code and examples**

Whether you’ve found a typo, discovered a more efficient algorithm, or built on one of the projects in a new way — we’d love to hear from you.

---

## Repository Structure

The repository is organized by source code (`src/`) and chapter folders (`ch_X/`), each containing the example projects and supporting files referenced in the book.

```text
📂 Embedded-AI/
├── LICENSE
├── README.md
├── data/
├── datasheets/
│   ├── ch_1/
│   ├── ch_3/
│   │   └── MCP6001 Op Amp
│   │   └── Pico C SDK
│   ├── ch_5/
│   ├── ch_7/
│   ├── ch_8/
│   ├── ch_9/
│   ├── ch_10/
│   ├── ch_12/
│   ├── ch_13/
│   └── ch_14/
├── schematics/
└── src/
    ├── ch_1/
    ├── ch_2/
    ├── ch_3/
    │   ├── bare-metal-blink/
    │   ├── pico-awg/
    │   ├── pico-awg-dma/
    │   └── pico-dma-irq/
    ├── ch_4/
    │   └── ...
    ├── ch_5/
    │   └── ...
    ├── ch_6/
    │   └── ...
    └── common/
        ├── utils/
        ├── data/
        └── models/
```
