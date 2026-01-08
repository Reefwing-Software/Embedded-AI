class Button {
  private:
    int pin;                   // The pin where the button is connected
    bool activeLow;            // True if the button is active low
    bool lastState;            // Last known state of the button
    bool currentState;         // Current debounced state of the button
    bool pressedFlag;          // Flag to indicate a new press
    bool releasedFlag;         // Flag to indicate a new release
    unsigned long lastDebounceTime; // Last time the button state changed
    unsigned long debounceDelay;    // Delay time for debounce (in milliseconds)
    void (*callback)();        // Pointer to callback function

    // Helper function to get the effective button state
    bool readButton() const {
      bool state = digitalRead(pin);
      return activeLow ? !state : state;  // Invert if activeLow
    }

  public:
    // Constructor to initialize button parameters with optional callback
    Button(int buttonPin, unsigned long debounceDelayMs = 20, bool isActiveLow = true, void (*onPressRelease)() = nullptr) 
      : pin(buttonPin), activeLow(isActiveLow), lastDebounceTime(0), debounceDelay(debounceDelayMs), 
        callback(onPressRelease), pressedFlag(false), releasedFlag(false) {

      pinMode(pin, INPUT_PULLUP); // Configure the button pin with internal pull-up
      currentState = lastState = readButton();  // Initialize to the actual button state
    }

    // Update the button state (call this method in loop)
    void update() {
      bool reading = readButton();  // Read the effective state of the button

      // Check if the button state has changed
      if (reading != lastState) {
        lastDebounceTime = millis();    // Reset the debounce timer
      }

      // If the debounce time has passed, update the current state
      if ((millis() - lastDebounceTime) > debounceDelay) {
        if (reading != currentState) {
          currentState = reading;       // Update the button state

          // Set flags for single detection of press and release
          if (currentState == HIGH) {
            pressedFlag = true;
          } else {
            releasedFlag = true;
          }

          // If a callback function is provided, call it when the button state changes
          if (callback != nullptr) {
            callback();
          }
        }
      }

      lastState = reading;  // Update the last state to the current reading
    }

    // Check if the button is currently pressed
    bool isPressed() const {
      return currentState == HIGH;
    }

    // Check if the button is currently released
    bool isReleased() const {
      return currentState == LOW;
    }

    // Check if the button was just pressed (single press detection)
    bool wasPressed() {
      if (pressedFlag) {
        pressedFlag = false; // Reset the flag after detecting the press
        return true;
      }
      return false;
    }

    // Check if the button was just released (single release detection)
    bool wasReleased() {
      if (releasedFlag) {
        releasedFlag = false; // Reset the flag after detecting the release
        return true;
      }
      return false;
    }

    // Return the last raw state of the button (before debounce logic)
    bool getLastState() const {
      return lastState;
    }
};