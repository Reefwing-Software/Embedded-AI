typedef void (*StateFunction)(); // Define a function pointer type for state functions
typedef void (*DisplayFunction)();

class StateMachine {
  private:
    struct State {
      String name;
      StateFunction function;
      DisplayFunction displayFunction;
    };

    State* states;
    int stateCount;
    int currentStateIndex;
    int maxStates;

  public:
    StateMachine(int maxStates) : maxStates(maxStates), stateCount(0), currentStateIndex(-1) {
      states = new State[maxStates];
    }

    ~StateMachine() {
      delete[] states;
    }

    // Add a new state with a name, run function, and display function
    void addState(const String& name, StateFunction function, DisplayFunction displayFunction) {
      if (stateCount < maxStates) {
        states[stateCount++] = {name, function, displayFunction};
      }
    }

    // Set the active state by name
    void setState(const String& name) {
      for (int i = 0; i < stateCount; i++) {
        if (states[i].name == name) {
          currentStateIndex = i;
          break;
        }
      }
    }

    // Run the active state's function, if any
    void run() {
      if (currentStateIndex >= 0 && currentStateIndex < stateCount) {
        if (states[currentStateIndex].function) {
          states[currentStateIndex].function();
        }
      }
    }

    // Run the active state's display function, if any
    void display() {
      if (currentStateIndex >= 0 && currentStateIndex < stateCount) {
        if (states[currentStateIndex].displayFunction) {
          states[currentStateIndex].displayFunction();
        }
      }
    }

    // Get the current state's name
    String getCurrentState() const {
      if (currentStateIndex >= 0 && currentStateIndex < stateCount) {
        return states[currentStateIndex].name;
      }
      return "";
    }
};