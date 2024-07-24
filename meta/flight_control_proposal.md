Proposal Template

The Pragmatic Programmers
https://pragprog.com

Thanks for choosing PragProg as your writing partner--we can't wait to read your proposal!

Please write your proposal in this template using standard Markdown (see https://www.markdownguide.org/basic-syntax) and send it to proposals@pragprog.com.

----

## Book Title: Build your own Arduino Flight Controller

## Book Subtitle (include keywords that aren't in the title):

## Author Name(s): David Such

## Page Count (your best estimate - allow 300 words to a page): 350 pages

## Overview

The genesis of this book was the need for a drone which could be used in schools and Universities to teach STEM (Science, Technology, Engineering and Math). We looked at several commercially available flight controllers and complete drones but none of them met all our criteria.  
 
<br> As we use Arduino® boards for our other robotic projects, we wanted to use the same hardware and tool chain to maximize the time spent learning the educational concepts required by the STEM curriculum. Our other requirements were:

* The drone needed to be able to be used safely within a school environment.
* The drone had to be able to be constructed by students using a 3D printed airframe and a kit of parts.
* The drone needed to be modular, open-source hardware and software and include an API to allow mission control and testing/tuning.
* The design philosophy was to provide the minimum functionality required to deliver the educational objectives.

We built a prototype based on commercially available parts and then designed our own airframe and flight controller, once we had a model that flew. We wanted a modular design where we could add optional functionality (e.g., FPV camera or GPS). Our design had space for these features but as we wanted to get something up and running as quickly as possible, our initial specification only included the minimum components required for a flyable drone (i.e., air frame, battery, power distribution, ESC, flight controller, receiver, motors, and propellers).

<br> As part of the educational process, we documented our design journey and explained the engineering choices that we have made along the way.

<br> While researching the best way to design a drone and its associated flight controller, we found that the available material was either too simplistic with the equivalent of blinking a LED / “Hello World” example, or a university level thesis targeting a very specific design issue. To assist others on a similar journey, we have tried to strike a middle ground between these two extremes, providing just the information you need.

<br> We wanted to use an Arduino as the flight controller hardware but there wasn’t any suitable firmware targeting this platform. Our initial plan was to port Betaflight to the Arduino Portenta H7, as this is designed for STM32 hardware, and we know that writing your own flight controller firmware is tough and time consuming. We managed to get Betaflight to compile for the H7 but because Arduino’s use a custom bootloader which is located right where Betaflight normally sits in memory, flashing the firmware was problematic. 

<br> Consequently, in addition to the hardware design, we have also written flight controller firmware targeting the ARDUINO PRO series of boards (i.e., Portenta H7, Nano 33 BLE, Nano 33 BLE SENSE, Nano 33 IoT and the Nano RP2040 Connect). These boards have sufficient speed, programming space and the interfaces required to sustain stable flight. A number also have onboard IMU’s which is a requirement for any flight controller.

<br> As we suspected, writing flight controller firmware is significantly harder than designing the hardware, particularly for a quadcopter. Drone hardware is very modular and there is a lot of information available on how to build your own. Things are different on the software side. There is information available, but it is fragmented, complicated and by its nature platform specific. We have tried to address this in our book. While our firmware is targeted at Arduino boards, we have tried to provide a simplistic Hardware Abstraction Layer (HAL) to make it easier to add new hardware. We have also attempted to explain what we are doing so the control architecture could be replicated in other programming languages.

<br> Interestingly, the original drone hackers used Arduino’s as their flight controller hardware, but as they added new features, they were constrained by the 8-bit processors and memory available on most of the Arduino boards at that time. As a result, developers moved to 32-bit processors, (e.g., STM32 based boards). To some extent, this book is taking us back to those earlier roots, now that there are Arduino boards available with sufficient capability. We believe there is still a hunger for people to be able to learn about drones by building their own and using hardware and software that they are familiar with.

<br> The book aims to strike a balance between overly simplistic beginner guides and highly technical academic theses. This makes it suitable for students, undergraduates, hobbyists, makers, and intermediate-level enthusiasts who have some technical background but are not experts. The book emphasizes understanding underlying concepts and principles. It does not just provide instructions but explains the reasoning behind design decisions and technical concepts. The book is focused on practical application, and it includes open-source code libraries for Arduino. The content builds up to the creation of a unique Arduino Flight Controller – called Raven. The hardware designs (schematics and PCBs) are also open-source.

<br> This book is the one your buy when all the others don’t answer the questions you have (e.g., should I write my own flight controller firmware or use an open-source or proprietary model? What do you decide on first, battery size, takeoff weight, motor size, propeller size? Do you need Sensor Fusion or data filtering? Do you use PID on a rate or on an angle? What should the flight controller do when the craft experiences signal loss, low battery, and other emergency situations?)


## Outline

    0.1 Preface	
        0.1.1 Drone Design Criteria
        0.1.2 Book Structure	
        0.1.3 Conventions Used in this Book	
        0.1.4 Code Examples and Permissions	
    0.2 Acronyms
    0.3 Symbols

Chapter 1 – Introduction to Drones

    1.1 Drone Components	
        1.1.1 Hardware & Electronics
        1.1.2 Software
            1.1.2.1 Stability & Control
            1.1.2.2 Safety & Failsafe	
            1.1.2.3 Guidance Layering
    1.2 Open-Source Flight Control Systems	
        1.2.1 The Flight Control Ecosystem
        1.2.2 The MultiWii Family
            1.2.2.1 MultiWii	
            1.2.2.2 BradWii	
            1.2.2.3 Baseflight
            1.2.2.4 Cleanflight
            1.2.2.5 Betaflight
            1.2.2.6 iNAV
            1.2.2.7 Raceflight/FlightOne
            1.2.2.8 Butterflight
            1.2.2.9 EmuFlight
        1.2.3 The OpenPilot Family
            1.2.3.1 OpenPilot
            1.2.3.2 LibrePilot
            1.2.3.3 Tau Labs	
            1.2.3.4 dRonin
        1.2.4 The DroneCode Foundation
            1.2.4.1 ArduPilot
            1.2.4.2 PX4
        1.2.5 Paparazzi
        1.2.6 Hackflight

    Chapter 2 - Multirotor Aerodynamics

    2.1 Propellers
        2.1.1 Terminology
        2.1.2 Theory of Flight
        2.1.3 Selecting Propellers
            2.1.3.1 Length & Aspect Ratio
            2.1.3.2 Pitch
            2.1.3.3 Blade Configuration
            2.1.3.4 Material
        2.1.4 Mounting Propellers
    2.2 Lift and Thrust
        2.2.1 Calculating Thrust from Motor Tables
        2.2.2 Ground Effect
    2.3 Multirotor Configurations
        2.3.1 Monocopter
        2.3.2 Bicopter
        2.3.3 Tricopter
        2.3.4 Quadcopter
        2.3.5 Pentacopter
        2.3.6 Hexacopter
        2.3.7 Octocopter
    2.4 Propeller Torque and Moment
    2.5 Ducts
    2.6 Controlling a Quadcopter
        2.6.1 Radio Control Transmitter Modes
        2.6.2 Control Concepts
        2.6.3 Altitude Control
        2.6.4 Pitching and Rolling
        2.6.5 Yawing using Angular Momentum
        2.6.6 Altitude Loss with Pitching and Rolling
    2.7 Drag
        2.7.1 Forces Acting on a Multirotor
        2.7.2 Parasitic and Induced Drag	
        2.7.3 Reducing Drag
    2.8 Vibration
        2.8.1 Why is Vibration a Problem?
        2.8.2 What causes Vibration in Drones?
        2.8.3 Techniques to Minimise Vibration
            2.8.3.1 Shock vs Vibration
            2.8.3.2 Hardware Solutions
            2.8.3.3 Software Solutions

    Chapter 3 – Energy Management & Charging

    3.1 Desirable Characteristics
    3.2 Battery Chemistry Options
    3.3 Charging LiPo’s
    3.3.1 Series and Parallel Cells
    3.3.2 Discharge Rate (C)	
    3.4 Battery Maintenance and Safety

    Chapter 4 – Hardware

    4.1 Power Supply Pin Terminology
    4.2 Switch Terminology	
    4.3 Communication Protocols
        4.3.1 Inter-Integrated Circuit (I2C) Serial	
        4.3.2 Serial Peripheral Interface (SPI)
        4.3.3 Universal Asynchronous Receiver / Transmitter (UART)
    4.4 Sensors
        4.4.1 The LPS22HB Pressure Sensor
            4.4.1.1 Register Mapping
            4.4.1.2 Interpreting Pressure Readings
            4.4.1.3 Interpreting Temperature Readings
            4.4.1.4 Determining Altitude from Air Pressure
        4.4.2 Writing an Arduino Library for the LPS22HB
            4.4.2.1 The Reefwing LPS22HB Library
            4.4.2.2 QNH, QFE and QNE
            4.4.2.3 Using the LPS22HB Library
            4.4.2.4 Library Public Methods
        4.4.3 The LSM9DS1 Inertial Measurement Unit
            4.4.3.1 The LSM9DS1 IMU
            4.4.3.2 LSM9DS1 Sample Rates (AKA Output Data Rate — ODR)
            4.4.3.3 LSM9DS1 Sensor Ranges	
            4.3.3.4 LSM9DS1 Arduino Libraries
        4.3.4 The Reefwing LSM9DS1 Arduino Library
            4.3.4.1 Register Mapping
            4.3.4.2 Who Am I?
            4.3.4.3 IMU Reset
            4.3.4.4 Gyroscope/Accelerometer Operating Modes
            4.3.4.5 Magnetometer Operating Modes
            4.3.4.6 IMU Configuration
            4.3.4.7 Configuration – Scale
            4.3.4.8 Configuration – Sample Rate (ODR)
            4.3.4.9 Configuration – Bandwidth
            4.3.4.10 Axis Orientation and Sign
            4.3.4.11 Enable Sensor Readings
            4.3.4.12 IMU Data Available
            4.3.4.13 Gyroscope and Accelerometer FIFO Registers
            4.3.4.14 Read Sensor Data - Temperature
            4.3.4.15 Bias Offset Calibration
            4.3.4.16 Gyroscope and Accelerometer Self-Test
            4.3.4.17 Magnetometer Self-Test
            4.3.4.18 Read Sensor Data - Gyroscope
        4.3.5 How to Use the Reefwing LSM9DS1 Library	

    Chapter 5 – Flight Controller Theory

    5.1 Why Would You?
    5.2 Target Hardware
        5.2.1 Arduino Pro Boards
        5.2.2 Other Options
    5.3 Flight Controller Overview
        5.3.1 Flight Modes
            5.3.1.1 Rate Mode
            5.3.1.2 Stabilize Mode
        5.3.2 Control Reference Frames
            5.3.2.1 Aircraft Reference Frame
            5.3.2.2 World Reference Frame
            5.3.2.3 Arduino Nano 33 BLE Reference Frame Conversion
            5.3.2.4 Converting from the Aircraft Reference Frame to NED
        5.3.3 Rate of Change of Euler Angles
        5.3.4 Inertial Navigation	
        5.3.5 PID Theory
            5.3.5.1 The Proportional Term
            5.3.5.2 The Integral Term
            5.3.5.3 The Derivative Term
    5.4 Flight Controller Components
        5.4.1 Pilot Input (SBUS)
            5.4.1.1 Binding the Receiver to the Transmitter
            5.4.1.2 The SBUS Protocol
            5.4.1.3 Inverting SBUS (Hardware)
            5.4.1.4 Arduino SBUS Library
        5.4.2 IMU Output to Roll, Pitch and Yaw
            5.4.2.1 Converting from a Gyro Rate to an Angle
            5.4.2.2 Converting from Accelerometer G force to a Roll Angle
            5.4.2.3 Converting Magnetometer Data to a Yaw Angle
            5.4.2.4 Compensating Magnetometer data for Hard and Soft Iron
        5.4.3 AHRS and Sensor Fusion
            5.4.3.1 Gyroscopic Drift, IMU Bias Offset, and Vibration Noise
            5.4.3.2 Sensor Fusion & Free Parameters
            5.4.3.3 The Classic Complementary Filter
            5.4.3.4 Calculating the Complementary Filter Coefficient (𝛂)
            5.4.3.5 Euler Angles
            5.4.3.6 Gimbal Lock
            5.4.3.7 Quaternions
            5.4.3.8 Complementary Filter using Quaternions	
            5.4.3.9 Madgwick Filter using Quaternions
            5.4.3.10 Mahony Explicit Complementary Filter using Quaternions	
            5.4.3.11 The Kalman Filter
        5.4.4 PID Control Loops
            5.4.4.1 Generating the Error Input
            5.4.4.2 What to Control? Angles or Rates?
        5.4.5 Motor Mixing and Outputs (ESC)
            5.4.5.1 Open Loop Motor Control
            5.4.5.2 Thrust Scaling
        5.4.6 ESC Motor Control	
            5.4.6.1 The Power Stage (3-Phase Bridge)
            5.4.6.2 MOSFET Drivers
            5.4.6.3 The Bootstrap Capacitor
            5.4.6.4 Zero-Crossing Detection
            5.4.6.5 Motor Current Monitoring
            5.4.6.6 The Differential Amplifier
            5.4.6.7 Operational Amplifier vs Current Sense Amplifier
        5.4.7 DC Motors
            5.4.7.1 Brushed DC Motors
                5.4.7.2 Brushed DC Motor Control
                5.4.7.3 The H-bridge
                5.4.7.4 Brushless DC Motors
                5.4.7.5 Brushless DC Motor Control
                5.4.7.6 Back EMF (BEMF)
                5.4.7.7 Start-up / Inrush Current	
                5.4.7.8 H-bridge Shoot Through
        5.4.8 Failsafe’s and Battery Monitoring
            5.4.8.1 Battery Monitoring
            5.4.8.2 Estimating State of Charge from Battery Voltage
            5.4.8.3 Failsafe
        5.4.9 Data Logging

    Chapter 6 - Received Signal Strength Indication (RSSI)

    Chapter 7 – The Raven Flight Controller

    7.1 Detecting Hardware
    7.2 Battery Monitoring
    7.3 ESC Control
    7.4 SBUS Communication
    7.5 IMU
    7.6 Flight Model and PID gain/limits
    7.7 Task Priority Management
    7.8 Testing

    Chapter 8 – MultiWii Serial Protocol

    8.1 The Reefwing Serial Protocol
    8.2 MultiWii Serial Protocol (MSP) v1
        8.2.1 Header
        8.2.2 Size
        8.2.3 Type
        8.2.4 Payload
        8.2.5 Checksum
    8.3 MSP v1 JUMBO Messages
    8.4 MSP Protocol Version 2 (MSPV2)
    8.5 The ReefwingMSP Arduino Library
        8.5.1 Library Examples
        8.5.2 Example 1 – View MSP Request
        8.5.3 Example 2 – View MSP Response
        8.5.4 The Reefwing Protocol Tester

    Index
    About the Author

## Bio

LinkedIn Profile: https://www.linkedin.com/in/davidsuch/
<br> Twitter/X: https://x.com/reefwing
<br> Medium: https://medium.com/@reefwing

<br> David Such is an Electrical Engineer and Director of Kintarla Pty Ltd, trading as Reefwing Software (www.reefwing.com.au). David delivers STEM training courses and his technical articles on: AI, IoT, Robotics, Drones, Raspberry Pi, Arduino, Python, C/C++, and Swift are available at - https://medium.com/@reefwing. 

<br> He is an Honorary Associate at the University of Sydney for his work on the Genesis Startup Program, Business Industry Mentoring Program, and the Faculty of Business Entrepreneurship: Lean Startup course. David provides advice as an Industry Expert for the Department of Education through their Careers NSW program.

<br> His qualifications are B.E. (Elec.), B.Sc. (Computer Science), B.App.Sc (Wine Making), and an MBA (Strategy). David holds a Remote Pilot Licence (RePL) and is endorsed for commercial multi-rotor operations. He also has an Aeronautical Radio Operator Certificate.

<br> Prior to this, David was Managing Director at Serco Australia from 2006 - April 2014. David was also an executive Director at Serco Australia Pty Ltd, Director at Serco Traffic Camera Services (VIC) from 2010-2014, Director at Excelior Pty Ltd, Director at DMS Maritime from 2010-2013, Director at Serco Sodexo Defence Services from 2010-2013, General Manager at ADT (security services) from 2002 - 2005 and Regional Manager/Engineer at Honeywell from 1987 - 2002.


## Competing Books

If you do a Google search for Arduino flight controller in Books, you get the following top 5 results:

1. "Make Your Arduino Quadcopter Drone from Scratch", Choice of Components, Construction of the Frame, Electrical and Electronic Wiring, Programming in Arduino Language of the Flight Controller. By Olivier Chau-Huu · 2021. This book is independently published and doesn't appear to be available for purchase.

2. Packt has four books about drones. All these books use pre-existing flight controller firmware and don’t go into the detail that my book does. There are many drone books that cover the easy subjects, mine describes the hard bits. This is the information you need once you get past building multirotor craft based on existing designs and software. Three of the four Packt books are quite old (2014, 2017, and 2018) and my book covers Arduino hardware which wasn’t available 2-3 years ago. This is important because Flight Controller software is demanding and the recent boards have the speed, memory and on-board sensors (e.g., IMU, barometer, and magnetometer) to make an Arduino based flight stack relatively easy to assemble.

3. "Make: Drones", Teach an Arduino to Fly. By David McGriffy · 2016. Another old book with outdated hardware, based on hacking commercially available drone which is no longer available.

4. "Design and Development of Arduino Drone". By Mohd Hazwan Mohd Puad, Wan Nur Hamimah Wan Hanipa · 2021. Another self published book. Very simplistic, and while it wasn't written long ago, it only covers the UNO R3.

5. "Arduino Flying Projects", How to Build Multicopters, from 100mm To 550mm. By ROBERT JAMES DAVIS (II.), Robert James Davis, II · 2017. Another out of date title.

There was a lot of books published on this subject about 10 years ago, but interest faded when the open source firmware moved to STM32 hardware. There are now a variety of 32 bit processors available on Arduino boards and I believe there is a latent demand for these types of projects.  

<br> I wrote this book because I couldn’t find the information anywhere else. To truly understand how to design a multirotor, you need sufficient theory to make intelligent decisions. Most books provide heuristics to make design decisions, my book explains where these rules come from and when you can safely ignore them.


## PragProg Books

I think the best category fit for this book would be **Hardware, Hobby, and Home**. The other Arduino and Raspberry Pi books would be relevant, although they may need an update.


## Market Size

The book was written to be part of a drone course used with STEM students. The book covers a wide range of topics including aerodynamics, electronics, programming, and control systems. This interdisciplinary approach is ideal for STEM. It would also appeal to the Arduino community, people who have moved beyond beginner-level projects and are looking for more challenging and comprehensive guides. They may have experience with simple Arduino projects and want to explore more complex applications like drone flight controllers.

The depth of detail would also be useful for undergraduate or graduate students in electrical engineering, robotics, or related fields who are looking for a practical, hands-on project to complement their theoretical studies. The book provides detailed explanations that can help bridge the gap between theory and real-world application.

As an indicator of market size, the ArduPilot website, a similar open-source flight controller, receives 8,600 daily visitors [Source](https://discuss.ardupilot.org/t/a-new-vision-for-ardupilot-org-insights-from-our-latest-analytics/107737). 

A selection of other websites showing interest on this subject:
-	https://www.instructables.com/DIY-ARDUINO-FLIGHT-CONTROLLER/
-	https://github.com/qqqlab/madflight
-	https://forum.arduino.cc/t/flight-controller-for-quadcopter/173573
-	https://www.hackster.io/akarsh98/flight-controller-tutorial-arduino-based-quadcopter-drone-8d752e
-	https://forum.flitetest.com/index.php?tags/arduino/



## Promotional Ideas

We have a marketing team who will help promote your book. What inside info can you give them? Think webinars, courses, conference talks, blogs, meet-up groups, anything you can participate in to promote your book. What ideas do you have?

## Writing Sample(s)





