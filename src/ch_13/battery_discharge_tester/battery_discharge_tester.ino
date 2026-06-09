/******************************************************************
  @file    battery_discharge_tester.ino
  @brief   Firmware for the Reefwing Battery Monitor and Logging Shield

  Version:     1.0.0

  Copyright (c) 2026 David Such

  This software is released under the MIT License.
  https://opensource.org/licenses/MIT  
******************************************************************/

#include <Wire.h>
#include <RTC.h>
#include <OPAMP.h>
#include <SD.h>
#include <SparkFunBQ27441.h>

#include "log.h"
#include "define.h"

RTCTime timeStamp(8, Month::NOVEMBER, 2024, 17, 44, 02, DayOfWeek::THURSDAY, SaveLight::SAVING_TIME_ACTIVE);
LogDestination* Log::destination = nullptr;
Log Log::logger;

float dischargeRate = DISCHARGE_MEDIUM;
unsigned long lastSampleTime = 0, sampleInterval = 30000; // 30 secs
unsigned int batteryVoltage = 0; // Last battery voltage measurement
const unsigned int BATTERY_CAPACITY = 1100; // 1100 mAh battery

void setupBQ27441() {
  if (!lipo.begin()) {
	// If communication fails, print an error message and loop forever.
    Log::logger.println(timeStamp, "Error - Unable to communicate with BQ27441");
    while (1) ;
  }

  Log::logger.println(timeStamp, "Connected to BQ27441");
  lipo.setCapacity(BATTERY_CAPACITY);
  batteryVoltage = lipo.voltage();
}

void setupOpAmp() {
  if (!OPAMP.begin(OPAMP_SPEED_HIGHSPEED)) {
    Log::logger.println(timeStamp, "Error - Failed to start op-amp");
  }
  else {
    bool const running = OPAMP.isRunning(0);

    if (running) {
      Log::logger.println(timeStamp, "Op-amp running on channel 0");
    } else {
      Log::logger.println(timeStamp, "Error - Op-amp on channel 0 is not running");
    }
  }
}

void setup() {
  pinMode(TEMP_PIN, INPUT);
  pinMode(GPOUT_PIN, INPUT);
  pinMode(CD, INPUT);
  pinMode(CE_PIN, OUTPUT);
  pinMode(DAC_PIN, OUTPUT);

  //  DAC - default 8-bit mode
  analogWriteResolution(8);
  analogWrite(DAC_PIN, 0);    // Turn off

  // CE is active low - turn it off
  digitalWrite(CE_PIN, HIGH);

  RTC.begin();
  RTC.setTime(timeStamp);

  // Log to Serial
  Serial.begin(115200);
  while (!Serial);

  Log::destination = new SerialDestination(Serial);
  Log::logger.println(timeStamp, "Logging to Serial");

  //  Battery Monitor
  setupBQ27441();

  // Op-amp
  setupOpAmp();

  // Set default discharge rate to slow
  setDischargeRate(dischargeRate);

  //  Sketch will only compile for an UNO R4
  #if defined(ARDUINO_UNOR4_MINIMA)
    Log::logger.println(timeStamp, "Board Detected: UNO R4 Minima");
  #elif defined(ARDUINO_UNOR4_WIFI)
    Log::logger.println(timeStamp, "Board Detected: UNO R4 WiFi");
  #else
    #error "This sketch is designed for the UNO R4"
  #endif
}

void setDischargeRate(float rate) {
    // Calculate the DAC voltage needed to achieve the target current
    float targetVoltage = rate * SENSE_RESISTOR;  

    // Map the target voltage to DAC range (0-255 for 0-5V on R4 Minima in 8-bit mode)
    int dacValue = (int)(targetVoltage * 256.0 / 5.0);

    dacValue = constrain(dacValue, 0, 255);  // Ensure within DAC limits

    Log::logger.println(timeStamp, "Current Discharge Rate: ", rate);
    Log::logger.println(timeStamp, "Target Voltage: ", targetVoltage);
    Log::logger.println(timeStamp, "DAC Value: ", dacValue);

    analogWrite(DAC_PIN, dacValue);  // Set DAC output
}

void sampleData() {
  if (millis() - lastSampleTime >= sampleInterval) {
    unsigned int soc = lipo.soc();  // state-of-charge (%)
    int current = lipo.current(AVG); // average current (mA)
    unsigned int fullCapacity = lipo.capacity(FULL); // full capacity (mAh)
    unsigned int capacity = lipo.capacity(REMAIN); // remaining capacity (mAh)
    int power = lipo.power(); // average power draw (mW)
    int health = lipo.soh(); // state-of-health (%)
    char data[100]; 

    batteryVoltage = lipo.voltage(); // battery voltage (mV)

    // Format the data into the character array using sprintf
    sprintf(data, "%d%% | %ld mV | %ld mA | %ld / %ld mAh | %ld mW | %d%%",
        soc, batteryVoltage, current, capacity, fullCapacity, power, health);

    // Log the data with the timestamp
    Log::logger.println(timeStamp, data);
    lastSampleTime = millis();
  }
}

void loop() {
  RTC.getTime(timeStamp);
  sampleData();
  if (batteryVoltage <= MIN_VOLTAGE) {
    Log::logger.println(timeStamp, "Battery discharged");
    analogWrite(DAC_PIN, 0);
    while (1) ;
  }
}
