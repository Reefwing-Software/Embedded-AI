/******************************************************************
  @file    battery_logger.ino
  @brief   Firmware for the Reefwing Battery Monitor and Logging Shield
  @author  David Such

  Version:     1.0.0
  Date:        18/11/24
******************************************************************/

#include <SPI.h>
#include <SD.h>
#include <RTC.h>
#include <U8g2lib.h>
#include <Wire.h>
#include <DHT11.h>
#include <OPAMP.h>
#include <SparkFunBQ27441.h>

#include "log.h"
#include "define.h"
#include "button.h"
#include "state_machine.h"
#include "structs.h"
#include "battery.h"

const SampleRate sampleRates[] = {
    {1, "Fast"},    // 1-second interval
    {30, "Medium"}, // 30-second interval
    {60, "Slow"}    // 60-second interval
};

const DischargeMode dischargeModes[] = {
    {"Slow",   0.2, 'S'},
    {"Medium", 0.5, 'M'},
    {"Fast",   0.8, 'F'}
};

int temperature = 0, humidity = 0;
int sampleRateIndex = 0, dischargeModeIndex = 0;
unsigned long lastSampleTime = 0, sampleInterval = 0; 
unsigned long setupTimeout = millis();

bool logToCard = false, cardAvailable = false;

unsigned long lastUpdate = 0;   // Timestamp for the last frequency update
unsigned int loopCount = 0;     // Counts the number of loop executions

char statusText[15];            // Character array to Temp, RH, and loop frequency

Battery battery(CE_PIN, DAC_PIN);
DHT11 dht11(TEMP_PIN);
StateMachine machine(9); // Create a state machine with 9 states
RTCTime timeStamp(18, Month::NOVEMBER, 2024, 10, 24, 00, DayOfWeek::MONDAY, SaveLight::SAVING_TIME_ACTIVE);
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

void sampleData() {
  // Lower sample rate accuracy better loop frequency
  if (millis() - lastSampleTime >= sampleInterval) {
    char data[100];
    int result = dht11.readTemperatureHumidity(temperature, humidity);
    unsigned int soc = lipo.soc();  // state-of-charge (%)
    int current = lipo.current(AVG); // average current (mA)
    unsigned int fullCapacity = lipo.capacity(FULL); // full capacity (mAh)
    unsigned int remainingCapacity = lipo.capacity(REMAIN); // remaining capacity (mAh)
    int power = lipo.power(); // average power draw (mW)
    int soh = lipo.soh(); // state-of-health (%)
    unsigned int voltage = lipo.voltage();

    if (soc <= 100) { // Check validity
      battery.fullCapacity = fullCapacity; // full capacity (mAh)
      battery.remainingCapacity = remainingCapacity; // remaining capacity (mAh) 
      battery.soc = soc;  // state-of-charge (%)
      battery.power = power; // average power draw (mW)
      battery.soh = soh; // state-of-health (%)
    }
    else {
      Log::logger.println(timeStamp, "Error: Invalid battery SOC detected.");
      machine.setState("ERROR");
    }

    if (voltage <= 4500) {
      battery.voltage = voltage; // battery voltage (mV)
    }
    else {
      Log::logger.println(timeStamp, "Error: Invalid battery voltage detected.");
      machine.setState("ERROR");
    }

    if (current > 0) {
      battery.current = current; // average current (mA)
    }
    else {
      Log::logger.println(timeStamp, "Error: Invalid battery current detected.");
      machine.setState("ERROR");
    }

    sprintf(data, "%d%% | %ld mV | %ld mA | %ld / %ld mAh | %ld mW | %d%% | %d°C | %d%%",
        battery.soc, battery.voltage, battery.current, battery.remainingCapacity, battery.fullCapacity, 
        battery.power, battery.soh, temperature, humidity);

    if (result != 0) {
      Log::logger.println(timeStamp, DHT11::getErrorString(result));
    }
    
    Log::logger.println(timeStamp, data);
    lastSampleTime = millis();
  }
}

bool checkTimeout(unsigned long &setupTimeout, unsigned long timeoutDuration = SETUP_TIMEOUT) {
    if (millis() - setupTimeout > timeoutDuration) {  // Check if timeout duration has passed
        Log::logger.println(timeStamp, "Timeout in setup state. Moving to MONITOR.");
        return true;
    }
    return false;
}

/******************************************************************
STATE MACHINE FUNCTIONS
******************************************************************/

void setupLog() {
  // Cycle through sample rates on mode button press
  if (modeButton.wasPressed()) {
    sampleRateIndex = (sampleRateIndex + 1) % 3;
    setupTimeout = millis();    // reset timeout
  }

  // Select sample rate and move to SETUP_DISCHARGE on start button press
  if (startButton.wasPressed()) {
    setupTimeout = millis();
    sampleInterval = sampleRates[sampleRateIndex].intervalSeconds * 1000;  // Convert to milliseconds
    Log::logger.print(timeStamp, "Sample Rate selected: ");
    Log::logger.println(sampleRates[sampleRateIndex].name);
    machine.setState("SETUP_DISCHARGE");
    return;
  }

  if (checkTimeout(setupTimeout)) {
    machine.setState("MONITOR");
    return;
  }

  // Check for log switch state change and SD card availability
  checkLogSwitch();
  checkCardState();
}

void setupLogDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  const char* cardText = CARD_TEXT(cardAvailable);
  char sampleRateText[15];

  snprintf(sampleRateText, sizeof(sampleRateText), "Log Rate: %ds", sampleRates[sampleRateIndex].intervalSeconds);

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
    setupTimeout = millis();
  }

  // Select discharge mode and move to MONITOR on start button press
  if (startButton.wasPressed()) {
    const DischargeMode& mode = dischargeModes[dischargeModeIndex];

    Log::logger.print(timeStamp, "Discharge Mode selected: ");
    Log::logger.println(mode.name);
    machine.setState("MONITOR");
    return;
  }

  if (checkTimeout(setupTimeout)) {
    machine.setState("MONITOR");
    return;
  }

  checkLogSwitch();
  checkCardState();
}

void setupDischargeDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  const char* cardText = CARD_TEXT(cardAvailable);
  char modeChar = dischargeModes[dischargeModeIndex].shortName;
  char dischargeModeText[15];

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

void monitor() {
  if (modeButton.wasPressed()) {
    machine.setState("CHARGE");
    return;  // Prevent further checks
  }

  if (startButton.wasPressed()) {
    machine.setState("SETUP_LOG");
    setupTimeout = millis();  // Reset the timeout
    return;
  }

  checkLogSwitch();
  sampleData();
}

void monitorDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char dataText[15];  // Room for 14 chars plus null terminator

  snprintf(dataText, sizeof(dataText), "%d%% %.1fV %dmA", battery.soc, battery.voltage / 1000.0, battery.current);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "MONITOR");
  u8g2.drawStr(0, 32, dataText);
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

void charge() {
  if (startButton.wasPressed()) {
    battery.startCharging();
    Log::logger.println(timeStamp, "Battery Charging");
    machine.setState("CHARGING");
    return;  
  }

  if (modeButton.wasPressed()) {
    machine.setState("DISCHARGE");
    return;
  }
}

void chargeDisplay() {
  const char* logText = LOG_TEXT(logToCard);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "CHARGE");
  u8g2.drawStr(0, 32, "Fast CHG 500mA");
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

void charging() {
  if (startButton.wasPressed()) {
    battery.stopCharging();    
    Log::logger.println(timeStamp, "Battery Charging stopped");

    if (battery.cycling) {
      battery.cycling = false;
      Log::logger.println(timeStamp, "Battery Cycling stopped");
      Log::logger.println(timeStamp, "Charge cycles: ", battery.chargeCycles);
      machine.setState("CYCLE");
      return;
    }

    machine.setState("CHARGE");
    return;
  }

  if (lipo.fcFlag()) {  //  Full charge detected
    battery.stopCharging();
    Log::logger.println(timeStamp, "Battery fully charged");

    if (battery.cycling) {
      battery.chargeCycles++;
      machine.setState("DISCHARGING");
      return;
    }

    machine.setState("MONITOR");
    return;
  }
}

void chargingDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char dataText[15];  // Room for 14 chars plus null terminator

  snprintf(dataText, sizeof(dataText), "%d%% %.1fV %dmA", battery.soc, battery.voltage / 1000.0, battery.current);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "CHARGING");
  u8g2.drawStr(0, 32, dataText);
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

void discharge() {
  if (startButton.wasPressed()) {
    float rate = dischargeModes[dischargeModeIndex].rate;
    
    battery.startDischarging(rate);
    Log::logger.println(timeStamp, "Battery Discharging");
    Log::logger.println("Current Discharge Rate (mA): ", rate * 1000);
    machine.setState("DISCHARGING");
    return;
  }

  if (modeButton.wasPressed()) {
    machine.setState("CYCLE");
    return;
  }
}

void dischargeDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char rateText[15];

  snprintf(rateText, sizeof(rateText), "Rate: %s", dischargeModes[dischargeModeIndex].name);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "DISCHARGE");
  u8g2.drawStr(0, 32, rateText);
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

void discharging() {
  if (startButton.wasPressed()) {
    battery.stopDischarging();    
    Log::logger.println(timeStamp, "Battery Discharging stopped");

    if (battery.cycling) {
      battery.cycling = false;
      Log::logger.println(timeStamp, "Battery Cycling stopped");
      Log::logger.println(timeStamp, "Charge cycles: ", battery.chargeCycles);
      machine.setState("CYCLE");
      return;
    }

    machine.setState("DISCHARGE");
    return;
  }

  if (battery.discharged()) {
    battery.stopDischarging();
    Log::logger.println(timeStamp, "Battery fully discharged");

    if (battery.cycling) {
      machine.setState("CHARGING");
      return;
    }

    machine.setState("MONITOR");
    return;
  }
}

void dischargingDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char dataText[15];  // Room for 14 chars plus null terminator

  snprintf(dataText, sizeof(dataText), "%d%% %.1fV %dmA", battery.soc, battery.voltage / 1000.0, battery.current);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "CHARGING");
  u8g2.drawStr(0, 32, dataText);
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

void cycle() {
  if (startButton.wasPressed()) {
    battery.chargeCycles = 0;
    battery.cycling = true;
    Log::logger.println(timeStamp, "Battery Cycling");
    machine.setState("CHARGING");
    return;
  }

  if (modeButton.wasPressed()) {
    machine.setState("MONITOR");
    return;
  }
}

void cycleDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char cycleText[15];  

  snprintf(cycleText, sizeof(cycleText), "Cycles: %u", battery.chargeCycles);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "CYCLE");
  u8g2.drawStr(0, 32, cycleText);
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

void error() {
  Log::logger.println(timeStamp, "System in error state. Charge/Discharging stopped.");
  battery.stopCharging();
  battery.stopDischarging();
}

void errorDisplay() {
  const char* logText = LOG_TEXT(logToCard);
  char cycleText[15];  

  snprintf(cycleText, sizeof(cycleText), "Cycles: %u", battery.chargeCycles);

  u8g2.clearBuffer();
  u8g2.drawStr(0, 0, "Log to SD:");
  u8g2.drawStr(101, 0, logText);
  u8g2.drawStr(0, 16, "<ERROR STATE>");
  u8g2.drawStr(0, 32, cycleText);
  u8g2.drawStr(0, 48, statusText);
  u8g2.sendBuffer();
}

/******************************************************************
SETUP
******************************************************************/

void setupLogging() {
  //  Check initial logSwitch and SD card state
  logSwitch.update();
  cardInserted.update();
  logToCard = logSwitch.isPressed();
  cardAvailable = cardInserted.isPressed();

  if (logToCard) {
    if (SD.begin(SPI_CS)) {  
      Log::destination = new SDCardDestination("log.txt");
      Log::logger.println(timeStamp, "Log to SD Card selected");
    }
    else {
      Serial.begin(115200);
      while (!Serial);

      Log::destination = new SerialDestination(Serial);
      Log::logger.println(timeStamp, "Logging to Serial");
      Log::logger.println(timeStamp, "Error - SD Card selected but not available");
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
}

void setupBQ27441() {
  if (!lipo.begin()) {
	// If communication fails, print an error message and loop forever.
    Log::logger.println(timeStamp, "Error - Unable to communicate with BQ27441");
    while (1) ;
  }

  Log::logger.println(timeStamp, "Connected to BQ27441");

  lipo.enterConfig(); 
  lipo.setCapacity(battery.capacity);
  lipo.setDesignEnergy(battery.capacity * 3.7f);
  lipo.exitConfig();

  battery.soc = lipo.soc();
  battery.voltage = lipo.voltage();
  battery.current = lipo.current(AVG);
  lastSampleTime = millis();
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

  RTC.begin();
  RTC.setTime(timeStamp);

  u8g2.begin();
  u8g2.setFont(u8g2_font_t0_17b_tr);  
  u8g2.setFontPosTop();

  setupLogging();

  //  Battery Monitor and op-amp
  battery.begin();
  setupBQ27441();
  setupOpAmp();

  // State Machine construction
  machine.addState("SETUP_LOG", setupLog, setupLogDisplay);
  machine.addState("SETUP_DISCHARGE", setupDischarge, setupDischargeDisplay);
  machine.addState("MONITOR", monitor, monitorDisplay);
  machine.addState("CHARGE", charge, chargeDisplay);
  machine.addState("CHARGING", charging, chargingDisplay);
  machine.addState("DISCHARGE", discharge, dischargeDisplay);
  machine.addState("DISCHARGING", discharging, dischargingDisplay);
  machine.addState("CYCLE", cycle, cycleDisplay);
  machine.addState("ERROR", error, errorDisplay);

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

void updateStatusText() {
  loopCount++;
  unsigned long currentTime = millis();
  
  if (currentTime - lastUpdate >= 1000) {
    snprintf(statusText, sizeof(statusText), "%d C %d%% %u Hz", temperature, humidity, loopCount);
    lastUpdate = currentTime;  // Update the timestamp for the next interval
    loopCount = 0;             // Reset the counter for the next second
  }
}

void loop() {
  updateStatusText();
  RTC.getTime(timeStamp);
  updateButtons();
  machine.run();
  machine.display();
}
