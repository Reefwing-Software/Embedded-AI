/******************************************************************
  @file    sd_card_tester.ino
  @brief   Firmware for the Reefwing Battery Monitor and Logging Shield

  Version:     1.0.0
 
  Copyright (c) 2026 David Such

  This software is released under the MIT License.
  https://opensource.org/licenses/MIT  
******************************************************************/

#include <SPI.h>
#include <SD.h>
#include <RTC.h>
#include <U8g2lib.h>
#include <Wire.h>
#include <DHT11.h>

#include "log.h"
#include "define.h"
#include "button.h"
#include "state_machine.h"

int sampleRates[] = {1, 30, 60};
int dischargeModes[] = {1, 2, 3}; // 1 = slow, 2 = medium, 3 = fast
int sampleRateIndex = 0;
int dischargeModeIndex = 0;
int selectedSampleRate = 1;
int selectedDischargeMode = 1;
int temperature = 0, humidity = 0;
bool logToCard = false, cardAvailable = false;
unsigned long lastSampleTime = 0, sampleInterval = 0; 

unsigned long lastUpdate = 0;  // Timestamp for the last frequency update
unsigned int loopCount = 0;    // Counts the number of loop executions
char loopFrequency[15];        // Character array to store the frequency text

DHT11 dht11(TEMP_PIN);
StateMachine machine(3); // Create a state machine with 3 states
RTCTime timeStamp(4, Month::NOVEMBER, 2024, 10, 15, 00, DayOfWeek::THURSDAY, SaveLight::SAVING_TIME_ACTIVE);
LogDestination* Log::destination = nullptr;
Log Log::logger;
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(/* rotation=*/U8G2_R0, /* reset=*/ U8X8_PIN_NONE);
Button modeButton(MODE_BTN), startButton(START_BTN);
Button logSwitch(LOG_SWITCH), ctrlSwitch(CTRL_SWITCH);
Button cardInserted(CD, 20, false);   // Unlike other switches this one is active high

void checkLogSwitch() {
  if (logSwitch.wasPressed()) {
    logToCard = true;
    Log::logger.println(timeStamp, "Log to SD Card selected");
  }
  else if (logSwitch.wasReleased()) {
    logToCard = false;
    Log::logger.println(timeStamp, "Log to Serial selected");
  }
}

void checkCardState() {
  if (cardInserted.wasPressed()) {
    cardAvailable = true;
    Log::logger.println(timeStamp, "SD card inserted");
  }
  else if (cardInserted.wasReleased()) {
    cardAvailable = false;
    Log::logger.println(timeStamp, "SD card removed");
  }
}

void setupLog() {
  // Cycle through sample rates on mode button press
  if (modeButton.wasPressed()) {
    sampleRateIndex = (sampleRateIndex + 1) % 3;
  }

  // Select sample rate and move to SETUP_DISCHARGE on start button press
  if (startButton.wasPressed()) {
    selectedSampleRate = sampleRates[sampleRateIndex];
    sampleInterval = selectedSampleRate * 1000;
    machine.setState("SETUP_DISCHARGE");
    Log::logger.println(timeStamp, "Sample Rate selected: ", sampleRates[sampleRateIndex]);
  }

  // Check for log switch state change and SD card availability
  checkLogSwitch();
  checkCardState();
}

void setupLogDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  const char* cardText = CARD_TEXT(cardAvailable);
  char sampleRateText[15];

  snprintf(sampleRateText, sizeof(sampleRateText), "Log Rate: %ds", sampleRates[sampleRateIndex]);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "SETUP LOG");
  u8g2.drawStr(0, 32, sampleRateText);
  u8g2.drawStr(0, 48, cardText);
  u8g2.sendBuffer();
}

void setupDischarge() {
  // Cycle through battery discharge modes on mode button press
  if (modeButton.wasPressed()) {
    dischargeModeIndex = (dischargeModeIndex + 1) % 3;
  }

  // Select discharge mode and move to MONITOR on start button press
  if (startButton.wasPressed()) {
    selectedDischargeMode = dischargeModes[dischargeModeIndex];
    machine.setState("MONITOR");
    Log::logger.print(timeStamp, "Discharge Mode selected: ");
    switch (selectedDischargeMode) {
      case 1: Log::logger.println("Slow"); break;
      case 2: Log::logger.println("Medium"); break;
      case 3: Log::logger.println("Fast"); break;
    }
  }

  checkLogSwitch();
  checkCardState();
}

void setupDischargeDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  const char* cardText = CARD_TEXT(cardAvailable);
  char modeChar;
  char dischargeModeText[15];

  // Determine the discharge mode based on the index
  switch (dischargeModes[dischargeModeIndex]) {
    case 1: modeChar = 'S'; break;  // Slow
    case 2: modeChar = 'M'; break;  // Medium
    case 3: modeChar = 'F'; break;  // Fast
    default: modeChar = '?'; break; // Unknown mode
  }

  // Format the discharge mode text
  snprintf(dischargeModeText, sizeof(dischargeModeText), "Discharge: %c", modeChar);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "DISCHARGE MODE");
  u8g2.drawStr(0, 32, dischargeModeText);
  u8g2.drawStr(0, 48, cardText);
  u8g2.sendBuffer();
}

void sampleData() {
  // Better sample rate accuracy slower loop frequency
  if (millis() >= lastSampleTime + sampleInterval) {
    int result = dht11.readTemperatureHumidity(temperature, humidity);

    if (result == 0) {
      Log::logger.println(timeStamp, "T: ", temperature, ", RH: ", humidity);
    } else {
      Log::logger.println(timeStamp, DHT11::getErrorString(result));
    }
    
    lastSampleTime += sampleInterval;
  }
}
/*
void sampleData() {
  // Lower sample rate accuracy better loop frequency
  if (millis() - lastSampleTime >= sampleInterval) {
    int result = dht11.readTemperatureHumidity(temperature, humidity);

    if (result == 0) {
      Log::logger.println(timeStamp, "T: ", temperature, ", RH: ", humidity);
    }
    else {
      Log::logger.println(timeStamp, DHT11::getErrorString(result));
    }
    lastSampleTime = millis();
  }
}*/

void monitor() {
  if (startButton.wasPressed()) {
    machine.setState("SETUP_LOG");
  }
  checkLogSwitch();
  sampleData();
}

void monitorDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char dataText[15];  // Room for 14 chars plus null terminator

  snprintf(dataText, sizeof(dataText), "T%d RH%d", temperature, humidity);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "MONITOR");
  u8g2.drawStr(0, 32, dataText);
  u8g2.drawStr(0, 48, loopFrequency);
  u8g2.sendBuffer();
}

void setup() {
  pinMode(TEMP_PIN, INPUT);
  pinMode(CE_PIN, OUTPUT);
  pinMode(GPOUT_PIN, INPUT);
  pinMode(CD, INPUT);

  RTC.begin();
  RTC.setTime(timeStamp);

  u8g2.begin();
  u8g2.setFont(u8g2_font_t0_17b_tr);  
  u8g2.setFontPosTop();

  //  Check initial logSwitch and SD card state
  logSwitch.update();
  cardInserted.update();
  logToCard = logSwitch.isPressed();
  cardAvailable = cardInserted.isPressed();

  if (logToCard) {
    if (!SD.begin(SPI_CS)) {  
      
    }
    else {
      Log::destination = new SDCardDestination("log.txt");
      Log::logger.println(timeStamp, "Log to SD Card selected");
    }
  }
  else {    // Log to Serial
    Serial.begin(115200);
    while (!Serial);

    Log::destination = new SerialDestination(Serial);
    Log::logger.println(timeStamp, "Logging to Serial");
  }

  //  Display logSwitch state
  char logText[20];

  snprintf(logText, sizeof(logText), "Log to SD Card: %s", LOG_TEXT(logToCard));
  Log::logger.println(timeStamp, logText);

  // State Machine construction
  machine.addState("SETUP_LOG", setupLog, setupLogDisplay);
  machine.addState("SETUP_DISCHARGE", setupDischarge, setupDischargeDisplay);
  machine.addState("MONITOR", monitor, monitorDisplay);

  machine.setState("SETUP_LOG");

  //  Sketch will only compile for an UNO R4
  #if defined(ARDUINO_UNOR4_MINIMA)
    Log::logger.println(timeStamp, "Board Detected: UNO R4 Minima");
  #elif defined(ARDUINO_UNOR4_WIFI)
    Log::logger.println(timeStamp, "Board Detected: UNO R4 WiFi");
  #else
    #error "This sketch is designed for the UNO R4"
  #endif
}

void updateButtons() {
  modeButton.update();
  startButton.update();
  logSwitch.update();
  ctrlSwitch.update();
  cardInserted.update();
}

void getLoopFreq() {
  loopCount++;
  unsigned long currentTime = millis();
  
  if (currentTime - lastUpdate >= 1000) {
    snprintf(loopFrequency, sizeof(loopFrequency), "Freq: %u Hz", loopCount);
    lastUpdate = currentTime;  // Update the timestamp for the next interval
    loopCount = 0;             // Reset the counter for the next second
  }
}

void loop() {
  getLoopFreq();
  RTC.getTime(timeStamp);
  updateButtons();
  machine.run();
  machine.display();
}
