@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
setlocal
REM go to the folder where this bat script is located
cd /d %~dp0

set ARDUINO_CLI=arduino-cli
set /A EXPECTED_CLI_MAJOR=0
set /A EXPECTED_CLI_MINOR=34
set /A EXPECTED_CLI_REV=2

set ARDUINO_CORE=arduino:mbed_nicla
set BOARD=%ARDUINO_CORE%:nicla_voice
set MBED_VERSION=4.0.8

where /q %ARDUINO_CLI%
IF ERRORLEVEL 1 (
    ECHO Cannot find 'arduino-cli' in your PATH. Install the Arduino CLI before you continue.
    ECHO Installation instructions: https://arduino.github.io/arduino-cli/latest/
    EXIT /B
)

REM parse arduino-cli version
FOR /F "tokens=1-3 delims==." %%I IN ('arduino-cli version') DO (
    FOR /F "tokens=1-3 delims== " %%X IN ('echo %%I') DO (
        set /A CLI_MAJOR=%%Z
    )
    SET /A CLI_MINOR=%%J
    FOR /F "tokens=1-3 delims== " %%X IN ('echo %%K') DO (
        set /A CLI_REV=%%X
    )
)

if !CLI_MAJOR! LEQ !EXPECTED_CLI_MAJOR! if !CLI_MINOR! LSS !EXPECTED_CLI_MINOR! GOTO UPGRADECLI

if !CLI_MAJOR! NEQ !EXPECTED_CLI_MAJOR! (
    echo You're using an untested version of Arduino CLI, this might cause issues (found: %CLI_MAJOR%.%CLI_MINOR%.%CLI_REV%, expected: %EXPECTED_CLI_MAJOR%.%EXPECTED_CLI_MINOR%.%EXPECTED_CLI_REV% )
) else (
    if !CLI_MINOR! NEQ !EXPECTED_CLI_MINOR! (
        echo You're using an untested version of Arduino CLI, this might cause issues (found: %CLI_MAJOR%.%CLI_MINOR%.%CLI_REV%, expected: %EXPECTED_CLI_MAJOR%.%EXPECTED_CLI_MINOR%.%EXPECTED_CLI_REV% )
    ) else (
        if !CLI_REV! NEQ !EXPECTED_CLI_REV! (
            echo You're using an untested version of Arduino CLI, this might cause issues (found: %CLI_MAJOR%.%CLI_MINOR%.%CLI_REV%, expected: %EXPECTED_CLI_MAJOR%.%EXPECTED_CLI_MINOR%.%EXPECTED_CLI_REV% )
        ) 
    )
)

set OUTPUT=""
for /f "delims=" %%i in ('arduino-cli config dump ^| findstr /r "user: "') do (
    set OUTPUT=%%i
)
IF "%OUTPUT%" == "" GOTO LIBRARYDIRNOTFOUND

set arduinodirectory=%OUTPUT:~8%%
set library=%OUTPUT:~8%\libraries
echo %arduinodirectory%

echo Finding Arduino Mbed Nicla %MBED_VERSION%...

set FOUND_VERSION=""
for /f "tokens=2 delims== " %%A in ('arduino-cli core list ^| findstr /r "%ARDUINO_CORE%"') do (
    set FOUND_VERSION=%%A
)
IF NOT %FOUND_VERSION% == %MBED_VERSION% GOTO INSTALLCOREVERSION

:ENDINSTALLCOREVERSION

for /f "delims=" %%i in ('arduino-cli config dump ^| findstr /r "data: "') do (
    set OUTPUT=%%i
)
IF "%OUTPUT%" == "" GOTO LIBRARYDIRNOTFOUND

echo Installing of libraries completed ...
@pause
exit /b 0

:NOTINPATHERROR
echo Cannot find 'arduino-cli' in your PATH. Install the Arduino CLI before you continue
echo Installation instructions: https://arduino.github.io/arduino-cli/latest/
@pause
exit /b 1

:UPGRADECLI
echo You need to upgrade your Arduino CLI version (now: %CLI_MAJOR%.%CLI_MINOR%.%CLI_REV%, but required: %EXPECTED_CLI_MAJOR%.%EXPECTED_CLI_MINOR%.x or higher)
echo See https://arduino.github.io/arduino-cli/installation/ for upgrade instructions
@pause
exit /b 1

:INSTALLCOREVERSION
echo Installing Nicla board ...
arduino-cli core update-index
arduino-cli core install %ARDUINO_CORE%@%MBED_VERSION%
echo Installing Nicla board OK
GOTO ENDINSTALLCOREVERSION

:LIBRARYDIRNOTFOUND
echo Arduino library directory not found. 
@pause
exit /b 1
