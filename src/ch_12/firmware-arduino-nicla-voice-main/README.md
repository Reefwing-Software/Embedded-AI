# firmware-arduino-nicla-voice
Firmware for Arduino Nicla Voice board

## Config build and flash

This project uses the `arduino-cli` compiler to build & flash new firmware. Windows users also need Arduino IDE (tested with v1.8.15).

### Usage - macOS and Linux

The script will verify if all needed libraries and the samd core is installed and install them if needed. If you prefer to do this 
step manually, follow the step in the next chapter.

For building the project:

* For audio support, use:
```
./arduino-build.sh --build
```

* For IMU sensor support, use:
```
./arduino-build.sh --build --with-imu
```

For flashing use:

```
./arduino-build.sh --flash
```


You can also do both by using:
```
./arduino-build.sh --all [--with-imu]
```

### Usage - Windows

* Run `update_libraries_windows.bat` script to install Arduino libraries.
* Note: the firwmare shall be located in a folder named `firmware-syntiant-nicla-internal`
* Note: Install version [0.21.0](https://github.com/arduino/arduino-cli/releases/tag/0.21.0) of the `arduino-cli`. Newer version are not supported yet. Download the [arduino-cli](https://github.com/arduino/arduino-cli/releases/download/0.21.0/arduino-cli_0.21.0_Windows_64bit.zip). For further instructions, see [Arduino cli installation](https://arduino.github.io/arduino-cli/0.21/installation/#download)

For building the project:

* For audio support, use:
```
./arduino-win-build.bat --build
```

* For IMU sensor support, use:
```
./arduino-win-build.bat --build --with-imu
```


For flashing use:

```
./arduino-win-build.bat --flash
```


You can also do both by using:
```
./arduino-win-build.bat --all [--with-imu]
```


### Flash NDP firmware and models

In order to be fully operative, the external flash of the board should be populated with:
- mcu_fw_120_v91.synpkg
- dsp_firmware_v91.synpkg
- ei_model.synpkg

#### Update using flash batch

There are 4 scripts for each supported OS:
- flash_<os> runs the mcu and the model flash script.
- flash_<os>_mcu flash just the firmware for the mcu.
- flash_<os>_model flash, if they are not present on the board, the NDP fw and the NDP dsp fw, and update the model.
- format_<os>_ext_flash erase the external flash.

where os can be linux, mac or windows.

To install the required dependencies, run the install_lib script for your os; you need to run isntall_lib just once.

The script to update the model uses one python package:
- pyserial https://pyserial.readthedocs.io/en/latest/
