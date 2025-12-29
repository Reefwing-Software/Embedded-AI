@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
setlocal
REM go to the folder where this bat script is located
cd /d %~dp0

set PROJECT=firmware-arduino-nicla-voice
set ARDUINO_CORE=arduino:mbed_nicla
set BOARD=%ARDUINO_CORE%:nicla_voice
set MBED_VERSION=4.0.8
set ARDUINO_CLI=arduino-cli
set BUILD_OPTION=--build
set FLASH_OPTION=--flash
set ALL_OPTION=--all

set SENSOR_WITH_IMU=--with-imu
:: use --with-imu flag as 2nd argument to build firmware for IMU
set COMMAND=%1
set SENSOR=%2

set /A EXPECTED_CLI_MAJOR=0
set /A EXPECTED_CLI_MINOR=34
set /A EXPECTED_CLI_REV=2

where /q %ARDUINO_CLI%
IF ERRORLEVEL 1 (
    ECHO Cannot find 'arduino-cli' in your PATH. Install the Arduino CLI before you continue.
    ECHO Installation instructions: https://arduino.github.io/arduino-cli/latest/
    EXIT /B
)

:: define and include
set DEFINE=-DARDUINOSTL_M_H -DEI_SENSOR_AQ_STREAM=FILE -DEI_PORTING_ARDUINO=1 -DMBED_NO_GLOBAL_USING_DIRECTIVE -O3
set INCLUDE=-I.\\src\\  -I.\\src\\ingestion-sdk -I.\\src\\ingestion-sdk-platform\\sensors\\ -I.\\src\\firmware-sdk\\ -I.\\src\\QCBOR\\inc\\ -I.\\src\\sensor_aq_mbedtls\\

if defined SENSOR (
    goto CHECKCOMMAND
)
:BACKHOME

:: just build
IF %COMMAND% == %BUILD_OPTION% goto :BUILD

:: look for connected board 
set COM_PORT=""
goto :FIND_COM_PORT
:COMM_FOUND

IF %COMMAND% == %FLASH_OPTION% goto :FLASH

IF %COMMAND% == %ALL_OPTION% goto :ALL else goto :COMMON_EXIT

echo No valid command

goto :COMMON_EXIT

:BUILD
    echo Building %PROJECT%
    echo %ARDUINO_CLI% compile -b %BOARD% --build-property "build.extra_flags=%DEFINE% %INCLUDE%"  --build-property "compiler.cpp.extra_flags=%CPP_FLAGS%" --output-dir .
    %ARDUINO_CLI% compile -b %BOARD% --build-property "build.extra_flags=%DEFINE% %INCLUDE%" --build-property "compiler.cpp.extra_flags=%CPP_FLAGS%" --output-dir .
goto :COMMON_EXIT

:FLASH
    echo Flashing %PROJECT%
    echo %ARDUINO_CLI% upload -p%COM_PORT% --fqbn %BOARD% --input-dir .
    %ARDUINO_CLI% upload -p%COM_PORT% --fqbn %BOARD% --input-dir .
goto :COMMON_EXIT

:ALL
    echo Building %PROJECT%
    echo %ARDUINO_CLI% compile --fqbn %BOARD% --build-property "build.extra_flags=%DEFINE% %INCLUDE%" --build-property "compiler.cpp.extra_flags=%CPP_FLAGS%" --output-dir .
    %ARDUINO_CLI% compile --fqbn %BOARD% --build-property "build.extra_flags=%DEFINE% %INCLUDE%" --build-property "compiler.cpp.extra_flags=%CPP_FLAGS%" --output-dir .
    echo Flashing %PROJECT%
    echo %ARDUINO_CLI% upload -p%COM_PORT% --fqbn %BOARD% --input-dir .
    %ARDUINO_CLI% upload -p%COM_PORT% --fqbn %BOARD% --input-dir .
goto :COMMON_EXIT

:: check for COM port and if they are listed as Arduino
:FIND_COM_PORT
echo Finding Arduino Nicla Voice...
for /f "tokens=1" %%i in ('arduino-cli board list ^| findstr "Nicla Voice" ^| findstr "COM"') do (
    set COM_PORT=%%i
)

IF %COM_PORT% == "" (
    echo Cannot find a connected Arduino Nicla Voice development board via 'arduino-cli board list'    
    @pause
    exit /b 1
)

echo FindingArduino Nicla Voice OK at %COM_PORT%
goto COMM_FOUND

:CHECKCOMMAND
if %SENSOR% == %SENSOR_WITH_IMU% (
    set DEFINE=-DARDUINOSTL_M_H -DEI_SENSOR_AQ_STREAM=FILE -DEI_PORTING_ARDUINO=1 -DMBED_NO_GLOBAL_USING_DIRECTIVE -O3 -DWITH_IMU
)

goto BACKHOME

:COMMON_EXIT