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

project(generator_test C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# include target library pico-tflmicro
add_subdirectory(
    ${CMAKE_CURRENT_SOURCE_DIR}/../pico-tflmicro
    ${CMAKE_CURRENT_BINARY_DIR}/pico-tflmicro
    EXCLUDE_FROM_ALL
)

# Add executable. Default name is the project name, version 0.1
add_executable(generator_test generator_test.cpp)

pico_set_program_name(generator_test "generator_test")
pico_set_program_version(generator_test "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(generator_test 0)
pico_enable_stdio_usb(generator_test 1)

# Add the required libraries to the build
target_link_libraries(
        generator_test
        pico-tflmicro
        pico_stdlib
)

# Add the standard include files to the build
target_include_directories(generator_test PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
)

pico_add_extra_outputs(generator_test)