/******************************************************************
   Serial Print Helper Class

   Usage:  log.println("Volts", 48.56, "Amps", 68);

 ******************************************************************/

class LogDestination {
  public:
    virtual void write(const char* message) = 0;
    virtual void writeLine(const char* message) = 0;  
};

class SerialDestination : public LogDestination {
  private:
    Stream& serial;  // Use Stream as the type for compatibility with Serial, SoftwareSerial, etc.

  public:
    // Constructor takes a reference to a Stream object (e.g., Serial)
    SerialDestination(Stream& serial) : serial(serial) {}

    void write(const char* message) override {
      serial.print(message);
    }

    void writeLine(const char* message) override {  
      serial.println(message);
    }
};

class SDCardDestination : public LogDestination {
  private:
    File logFile;
    const char* filename;

  public:
    SDCardDestination(const char* filename) : filename(filename) {
      logFile = SD.open(filename, FILE_WRITE);
      if (!logFile) {
        Serial.println("Failed to open file for writing");
      }
    }

    void write(const char* message) override {
      if (logFile) {
        logFile.print(message);
        logFile.flush();  // Ensure data is written to the SD card
      }
    }

    void writeLine(const char* message) override {
      if (logFile) {
        logFile.println(message);
        logFile.flush();
      }
    }

    ~SDCardDestination() {
      if (logFile) {
        logFile.close();  // Close the file when done
      }
    }
};

class Log {
  public:
    static LogDestination* destination;
    static Log logger;

    template<typename... Args>
    void print(Args&&... args) {
      if (destination) {
        logImpl<false>(args...);
      }
    }

    template<typename... Args>
    void println(Args&&... args) {
      if (destination) {
        logImpl<true>(args...);
      }
    }

  private:
    template<bool newline, typename X>
    void logImpl(X&& x) {
      // if the message is longer than 64 bytes, it will be truncated, 
      // and only the first 63 characters will be logged (with one byte 
      // reserved for the null-terminator '\0')
      char buffer[64];
      snprintf(buffer, sizeof(buffer), "%s", String(x).c_str());
      destination->write(buffer);
      if (newline) destination->writeLine("");
    }

    template<bool newline, typename X, typename... Args>
    void logImpl(X&& x, Args&&... args) {
      char buffer[64];
      snprintf(buffer, sizeof(buffer), "%s", String(x).c_str());
      destination->write(buffer);
      destination->write(" ");
      logImpl<newline>(args...);
    }
};