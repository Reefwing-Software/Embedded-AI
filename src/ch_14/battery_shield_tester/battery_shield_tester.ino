/******************************************************************
  @file    battery_shield_tester.ino
  @brief   Firmware for the Reefwing Battery Monitor and Logging Shield
  @author  David Such

  Version:     1.0.0
  Date:        07/11/24
******************************************************************/

#include <Wire.h>
#include <RTC.h>
#include <OPAMP.h>
#include <SD.h>
#include <SparkFunBQ27441.h>

#include "log.h"
#include "define.h"

RTCTime timeStamp(7, Month::NOVEMBER, 2024, 10, 15, 00, DayOfWeek::THURSDAY, SaveLight::SAVING_TIME_ACTIVE);
LogDestination* Log::destination = nullptr;
Log Log::logger;

unsigned long lastSampleTime = 0, sampleInterval = 30000; // 30 secs
const unsigned int BATTERY_CAPACITY = 1100; // 1100mAh battery

void setupBQ27441(void) {
  if (!lipo.begin()) {
	// If communication fails, print an error message and loop forever.
    Log::logger.println(timeStamp, "Error - Unable to communicate with BQ27441");
    while (1) ;
  }

  Log::logger.println(timeStamp, "Connected to BQ27441");
  lipo.setCapacity(BATTERY_CAPACITY);
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
  OPAMP.begin(OPAMP_SPEED_HIGHSPEED);

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

  //  Sketch will only compile for an UNO R4
  #if defined(ARDUINO_UNOR4_MINIMA)
    Log::logger.println(timeStamp, "Board Detected: UNO R4 Minima");
  #elif defined(ARDUINO_UNOR4_WIFI)
    Log::logger.println(timeStamp, "Board Detected: UNO R4 WiFi");
  #else
    #error "This sketch is designed for the UNO R4"
  #endif

}

void sampleData() {
  if (millis() - lastSampleTime >= sampleInterval) {
    unsigned int soc = lipo.soc();  // state-of-charge (%)
    unsigned int volts = lipo.voltage(); // battery voltage (mV)
    int current = lipo.current(AVG); // average current (mA)
    unsigned int fullCapacity = lipo.capacity(FULL); // full capacity (mAh)
    unsigned int capacity = lipo.capacity(REMAIN); // remaining capacity (mAh)
    int power = lipo.power(); // average power draw (mW)
    int health = lipo.soh(); // state-of-health (%)
    char data[100]; 

    // Format the data into the character array using sprintf
    sprintf(data, "%d%% | %ld mV | %ld mA | %ld / %ld mAh | %ld mW | %d%%",
        soc, volts, current, capacity, fullCapacity, power, health);

    // Log the data with the timestamp
    Log::logger.println(timeStamp, data);
    lastSampleTime = millis();
  }
}

void loop() {
  RTC.getTime(timeStamp);
  sampleData();
}
