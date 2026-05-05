# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.0)
set(toolchainVersion 13_3_Rel1)
set(picotoolVersion 2.1.0)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(pico-usb-midi C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1
add_executable(pico-usb-midi
  pico-usb-midi.c
  usb_descriptors.c
)

pico_set_program_name(pico-usb-midi "pico-usb-midi")
pico_set_program_version(pico-usb-midi "0.1")

# Create C header file with the name <pio program>.pio.h
pico_generate_pio_header(${PROJECT_NAME}  
        ${CMAKE_CURRENT_LIST_DIR}/touch.pio
)

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_usb(pico-usb-midi 0)
pico_enable_stdio_uart(pico-usb-midi 1)

# Add the standard include files to the build
target_include_directories(pico-usb-midi PRIVATE ${CMAKE_CURRENT_LIST_DIR})

# Add the standard library to the build
target_link_libraries(pico-usb-midi PRIVATE 
    pico_stdlib 
    hardware_pio
    tinyusb_device 
    tinyusb_board
)

pico_add_extra_outputs(pico-usb-midi)