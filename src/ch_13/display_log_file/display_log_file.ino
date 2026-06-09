/******************************************************************
  @file    display_log_file.ino
  @brief   Display the contents of log.txt on the Serial Monitor

  Version:     1.0.0
  
  Copyright (c) 2026 David Such

  This software is released under the MIT License.
  https://opensource.org/licenses/MIT  
******************************************************************/

#include <SPI.h>
#include <SD.h>

const int chipSelect = 10; // Pin for SD card chip select
const char *logFileName = "log.txt";

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for serial connection
  }

  // Initialize SD card
  if (!SD.begin(chipSelect)) {
    Serial.println("Error: SD card initialization failed!");
    return;
  }
  
  Serial.println("SD card initialized.");
  displayCommands();
  
  // Display the log file contents on startup
  displayLogFile();
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    switch (command) {
      case '\n':
      case '\r':
        // Ignore carriage return character
        break;
      case 'v':
        displayLogFile();
        break;
        
      case 'd':
        deleteLogFile();
        break;

      default:
        Serial.println("Unknown command.");
        displayCommands();
        break;
    }
  }
}

void displayCommands() {
  Serial.println("Available commands:");
  Serial.println("'v' - View the log file");
  Serial.println("'d' - Delete the log file");
}

void displayLogFile() {
  if (SD.exists(logFileName)) {
    File logFile = SD.open(logFileName, FILE_READ);
    if (logFile) {
      Serial.println("Displaying contents of log.txt:");
      while (logFile.available()) {
        Serial.write(logFile.read());
      }
      logFile.close();
      Serial.println(); // Add a newline after displaying the file
    } else {
      Serial.println("Error: Failed to open log.txt.");
    }
  } else {
    Serial.println("Log file not found.");
  }
}

void deleteLogFile() {
  if (SD.exists(logFileName)) {
    if (SD.remove(logFileName)) {
      Serial.println("Log file deleted successfully.");
    } else {
      Serial.println("Error: Failed to delete log file.");
    }
  } else {
    Serial.println("Log file not found.");
  }
}