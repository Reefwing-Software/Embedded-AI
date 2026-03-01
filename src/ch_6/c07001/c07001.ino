/******************************************************************
  @file       c07001.ino
  @brief      Temperature compressed sensing
  @author     David Such
  @copyright  Please see the accompanying LICENSE file

  Code:        David Such
  Version:     1.0.0
  Date:        01/10/24

  1.0.0     Original Release.       01/10/24

******************************************************************/

#include <DHT11.h>

#define DHTPIN 2      // DHT11 data pin connected to D2 on the Arduino

DHT11 dht11(DHTPIN);  // Create an instance of the DHT11 class

const int numSamples = 100;        // Total number of possible samples (e.g., for 100 seconds)
const int compressedSamples = 20;  // Number of random compressed samples

int regularSamples[numSamples];  // Store regular samples (taken every second)
int compressedSamplesData[compressedSamples];  // Store compressed samples
int randomIndices[compressedSamples];  // Store random sample indices for compressed sensing

void setup() {
  //  Start Serial and wait for connection
  Serial.begin(115200);
  while (!Serial);

  // Generate random indices for compressed sensing (undersampling)
  for (int i = 0; i < compressedSamples; i++) {
    int rnd;
    bool unique;
    do {
      rnd = random(0, numSamples);
      unique = true;
      for (int j = 0; j < i; j++) {
        if (randomIndices[j] == rnd) {
          unique = false;
          break;
        }
      }
    } while (!unique);
    randomIndices[i] = rnd;
  }

  Serial.println("Sampling data from DHT11 sensor...");
}

void loop() {
  static int sampleIndex = 0;

  if (sampleIndex < numSamples) {
    // Take a sample every second for regular sampling
    int temperature = dht11.readTemperature();

    // Check if the sensor data is valid
    if (temperature == DHT11::ERROR_CHECKSUM || temperature == DHT11::ERROR_TIMEOUT) {
      Serial.println(DHT11::getErrorString(temperature));
      return;
    }

    // Store regular samples
    regularSamples[sampleIndex] = temperature;

    // Check if this sample should be saved as part of the compressed samples
    for (int i = 0; i < compressedSamples; i++) {
      if (sampleIndex == randomIndices[i]) {
        compressedSamplesData[i] = temperature;
      }
    }

    // Output the regular sample to the Serial Monitor
    Serial.print("Sample ");
    Serial.print(sampleIndex);
    Serial.print(": ");
    Serial.print(temperature);
    Serial.println(" °C");

    sampleIndex++;
    delay(600000);  // Delays for 10 minutes
  } 
  else {
    // Output the compressed samples after collection is complete
    Serial.println("\nCompressed Samples (randomly selected):");
    for (int i = 0; i < compressedSamples; i++) {
      Serial.print("Sample ");
      Serial.print(randomIndices[i]);
      Serial.print(": ");
      Serial.print(compressedSamplesData[i]);
      Serial.println(" °C");
    }

    // Output the full regular sample list for comparison
    Serial.println("\nAll Regular Samples (for comparison):");
    for (int i = 0; i < numSamples; i++) {
      Serial.print("Sample ");
      Serial.print(i);
      Serial.print(": ");
      Serial.print(regularSamples[i]);
      Serial.println(" °C");
    }

    // Stop acquisition once all the data has been collected and printed
    while (true);
  }

} 
