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

project(blink C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# include target library pico-tflmicro
add_subdirectory(
    ${CMAKE_CURRENT_SOURCE_DIR}/../pico-tflmicro
    ${CMAKE_CURRENT_BINARY_DIR}/pico-tflmicro
    EXCLUDE_FROM_ALL
)

# Add executable. Default name is the project name, version 0.1
add_executable(blink blink.cpp)

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(blink 0)
pico_enable_stdio_usb(blink 1)

# pull in common dependencies
target_link_libraries(
    blink 
    pico-tflmicro
    pico_stdlib
)

if (PICO_CYW43_SUPPORTED)
    target_link_libraries(blink pico_cyw43_arch_none)
endif()

# Add the standard include files to the build
target_include_directories(blink PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
)

# create map/bin/hex file etc.
pico_add_extra_outputs(blink)

# add url via pico_set_program_url
