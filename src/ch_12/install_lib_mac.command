#!/bin/bash

# used for grepping
ARDUINO_CORE="arduino:mbed_nicla"
ARDUINO_CORE_VERSION="4.0.8"

BOARD="${ARDUINO_CORE}":nicla_voice

if [ -z "$ARDUINO_CLI" ]; then
	ARDUINO_CLI=$(which arduino-cli || true)
fi

EXPECTED_CLI_MAJOR=0
EXPECTED_CLI_MINOR=34
EXPECTED_CLI_REV=2

if [ ! -x "$ARDUINO_CLI" ]; then
    echo "Cannot find 'arduino-cli' in your PATH. Install the Arduino CLI before you continue."
    echo "Installation instructions: https://arduino.github.io/arduino-cli/latest/"
    exit 1
fi

CLI_MAJOR=$($ARDUINO_CLI version | cut -d. -f1 | rev | cut -d ' '  -f1)
CLI_MINOR=$($ARDUINO_CLI version | cut -d. -f2)
CLI_REV=$($ARDUINO_CLI version | cut -d. -f3 | cut -d ' '  -f1)

# if (( CLI_MINOR < EXPECTED_CLI_MINOR)); then
#     echo "You need to upgrade your Arduino CLI version (now: $CLI_MAJOR.$CLI_MINOR.$CLI_REV, but required: $EXPECTED_CLI_MAJOR.$EXPECTED_CLI_MINOR.x or higher)"
#     echo "See https://arduino.github.io/arduino-cli/installation/ for upgrade instructions"
#     exit 1
# fi

if (( CLI_MAJOR != EXPECTED_CLI_MAJOR || CLI_MINOR != EXPECTED_CLI_MINOR || CLI_REV != EXPECTED_CLI_REV)); then
    echo "You're using an untested version of Arduino CLI, this might cause issues (found: $CLI_MAJOR.$CLI_MINOR.$CLI_REV, expected: $EXPECTED_CLI_MAJOR.$EXPECTED_CLI_MINOR.$EXPECTED_CLI_REV)"
fi

# Check for libraries
# Board lib
has_mbed_core() {
    $ARDUINO_CLI core list | grep -e "${ARDUINO_CORE}.*${ARDUINO_CORE_VERSION}"
}
HAS_ARDUINO_CORE="$(has_mbed_core)"

if [ -z "$HAS_ARDUINO_CORE" ]; then
    echo not found
    echo "Installing Arduino Nicla Voice core..."
    $ARDUINO_CLI core update-index
    $ARDUINO_CLI core install "${ARDUINO_CORE}@${ARDUINO_CORE_VERSION}"
    echo "Installing Arduino Nicla Voice core OK"
fi

echo "Installing python packages"
pip3 install pyserial
echo "Done"
