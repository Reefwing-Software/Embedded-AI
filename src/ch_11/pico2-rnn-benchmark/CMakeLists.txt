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
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico2 CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(pico2-rnn-benchmark C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add RNNoise library
add_library(rnnoise STATIC
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/celt_lpc.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/denoise.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/kiss_fft.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/pitch.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/rnn.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/rnn_data.c
)

target_include_directories(rnnoise PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/include
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src
)

# Add executable. Default name is the project name, version 0.1
add_executable(pico2-rnn-benchmark pico2-rnn-benchmark.c)

pico_set_program_name(pico2-rnn-benchmark "pico2-rnn-benchmark")
pico_set_program_version(pico2-rnn-benchmark "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(pico2-rnn-benchmark 0)
pico_enable_stdio_usb(pico2-rnn-benchmark 1)

# Add the standard library to the build
target_link_libraries(pico2-rnn-benchmark
        pico_stdlib
        rnnoise
)

# Add the standard include files to the build
target_include_directories(pico2-rnn-benchmark PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
)

pico_add_extra_outputs(pico2-rnn-benchmark)

