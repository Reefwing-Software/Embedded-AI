/******************************************************************
  @file    calibrate.ino
  @brief   Adjust slow, medium, and fast battery discharge current
  @author  David Such

  Version:     1.0.0
  Date:        16/11/24
******************************************************************/

#include <SPI.h>
#include <SD.h>
#include <RTC.h>
#include <U8g2lib.h>
#include <Wire.h>
#include <DHT11.h>
#include <OPAMP.h>
#include <EEPROM.h>
#include <SparkFunBQ27441.h>

#include "log.h"
#include "define.h"
#include "button.h"
#include "state_machine.h"
#include "structs.h"

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