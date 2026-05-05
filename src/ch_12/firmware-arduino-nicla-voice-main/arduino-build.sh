#!/bin/bash
# -fqbn=arduino-git:mbed:nicla_voice

PROJECT=firmware-arduino-nicla-voice
COMMAND=$1
# use --with-imu flag as 2nd argument to build firmware for IMU
SENSOR=$2

# used for grepping
ARDUINO_CORE="arduino:mbed_nicla"
ARDUINO_CORE_VERSION="4.0.8"

BOARD="${ARDUINO_CORE}":nicla_voice

if [ -z "$ARDUINO_CLI" ]; then
	ARDUINO_CLI=$(which arduino-cli || true)
fi

DIRNAME="$(basename "$SCRIPTPATH")"
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

if ((CLI_MAJOR <= EXPECTED_CLI_MAJOR && CLI_MINOR < EXPECTED_CLI_MINOR)); then
    echo "You need to upgrade your Arduino CLI version (now: $CLI_MAJOR.$CLI_MINOR.$CLI_REV, but required: $EXPECTED_CLI_MAJOR.$EXPECTED_CLI_MINOR.$EXPECTED_CLI_REV or higher)"
    echo "See https://arduino.github.io/arduino-cli/installation/ for upgrade instructions"
    exit 1
fi

if (( CLI_MAJOR != EXPECTED_CLI_MAJOR || CLI_MINOR != EXPECTED_CLI_MINOR || CLI_REV != EXPECTED_CLI_REV)); then
    echo "You're using an untested version of Arduino CLI, this might cause issues (found: $CLI_MAJOR.$CLI_MINOR.$CLI_REV, expected: $EXPECTED_CLI_MAJOR.$EXPECTED_CLI_MINOR.$EXPECTED_CLI_REV)"
fi

# parses Arduino CLI's (core list and lib list) output and returns the installed version.
# Expected format (spaces can vary):
#    <package/core>   <installed version>  <latest version>  <other>
#
parse_installed() {
    echo "${1}" | awk -F " " '{print $2}' || true
}

# finds a Arduino core installed and returns the version
# otherwise it returns empty string
#
find_arduino_core() {
    core=$1
    version=$2
    result=""
    # space intentional
    line="$($ARDUINO_CLI core list | grep "${core} " || true)"
    if [ -n "$line" ]; then
        installed="$(parse_installed "${line}")"
        if [ "$version" = "$installed" ]; then
           result="$installed"
        fi
    fi
    echo $result
}

HAS_ARDUINO_CORE="$(find_arduino_core "${ARDUINO_CORE}" "${ARDUINO_CORE_VERSION}")"

if [ -z "$HAS_ARDUINO_CORE" ]; then
    echo not found
    echo "Installing Arduino Nicla Voice core..."
    $ARDUINO_CLI core update-index
    $ARDUINO_CLI core install "${ARDUINO_CORE}@${ARDUINO_CORE_VERSION}"
    echo "Installing Arduino Nicla Voice core OK"
fi

# Include path
INCLUDE="-I ./src"
INCLUDE+=" -I./src/ingestion-sdk"
INCLUDE+=" -I./src/ingestion-sdk-platform/sensors"
INCLUDE+=" -I./src/firmware-sdk"
INCLUDE+=" -I ./src/QCBOR/inc"
INCLUDE+=" -I ./src/sensor_aq_mbedtls"
# Flags
FLAGS="-DARDUINOSTL_M_H"
FLAGS+=" -O1"
FLAGS+=" -DEI_SENSOR_AQ_STREAM=FILE"
FLAGS+=" -DEI_PORTING_ARDUINO=1"

if [ "$SENSOR" = "--with-imu" ];
then    
    CPP_FLAGS="-DWITH_IMU"
else
    CPP_FLAGS=""
fi

if [ "$COMMAND" = "--build" ];
then
    echo "Building $PROJECT"
    arduino-cli compile --fqbn  $BOARD --build-property build.extra_flags="$INCLUDE $FLAGS" --build-property "compiler.cpp.extra_flags=${CPP_FLAGS}" --output-dir . &
    pid=$! # Process Id of the previous running command
    while kill -0 $pid 2>/dev/null
    do
        echo "Still building..."
        sleep 2
    done
    wait $pid
    ret=$?
    if [ $ret -eq 0 ]; then
        echo "Building $PROJECT done"
    else
        exit "Building $PROJECT failed"
    fi
elif [ "$COMMAND" = "--flash" ];
then
    echo "Flashing board"
    arduino-cli upload --fqbn  $BOARD
elif [ "$COMMAND" = "--all" ];
then
    echo "Building and flashing $PROJECT"
    echo "Building $PROJECT"
    arduino-cli compile --fqbn  $BOARD --build-property build.extra_flags="$INCLUDE $FLAGS" --build-property "compiler.cpp.extra_flags=${CPP_FLAGS}" --output-dir . &
    pid=$! # Process Id of the previous running command
    while kill -0 $pid 2>/dev/null
    do
        echo "Still building..."
        sleep 2
    done
    wait $pid
    ret=$?
    if [ $ret -eq 0 ]; then
        echo "Building $PROJECT done"
        echo "Flashing board"
        arduino-cli upload --fqbn  $BOARD
    else
        exit "Building $PROJECT failed"
    fi
else
    echo "Nothing to do for target"
fi