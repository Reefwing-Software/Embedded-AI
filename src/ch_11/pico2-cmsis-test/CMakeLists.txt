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

project(pico2-cmsis-test C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add CMSIS headers globally before building DSP
include_directories(
    lib/CMSIS/CMSIS_6/CMSIS/Core/Include
    lib/CMSIS/headers
)

# Now add CMSIS-DSP
set(ARM_MATH_CM33 ON)  # tell CMSIS-DSP to build Cortex-M33
add_subdirectory(lib/CMSIS/CMSIS-DSP)

# Build the arm_cortexM33_math library manually
file(GLOB CMSIS_DSP_SRC
    lib/CMSIS/CMSIS-DSP/Source/BasicMathFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/TransformFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/CommonTables/*.c
    lib/CMSIS/CMSIS-DSP/Source/FastMathFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/StatisticsFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/MatrixFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/ComplexMathFunctions/*.c
)

# Remove NEON-specific files that won't compile for M33
list(REMOVE_ITEM CMSIS_DSP_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/lib/CMSIS/CMSIS-DSP/Source/MatrixFunctions/_arm_mat_mult_neon.c
    ${CMAKE_CURRENT_SOURCE_DIR}/lib/CMSIS/CMSIS-DSP/Source/ComplexMathFunctions/_arm_cmplx_mult_neon.c
)

# Create the math library
add_library(arm_cortexM33_math ${CMSIS_DSP_SRC})

# Set include paths for CMSIS-DSP
target_include_directories(arm_cortexM33_math PUBLIC
    lib/CMSIS/CMSIS-DSP/Include
    lib/CMSIS/CMSIS_6/CMSIS/Core/Include
    lib/CMSIS/headers
)

# Compile definitions
target_compile_definitions(arm_cortexM33_math PUBLIC
    ARM_MATH_CM33
    ARM_MATH_LOOPUNROLL
)

# Add executable. Default name is the project name, version 0.1
add_executable(pico2-cmsis-test pico2-cmsis-test.c )

pico_set_program_name(pico2-cmsis-test "pico2-cmsis-test")
pico_set_program_version(pico2-cmsis-test "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(pico2-cmsis-test 0)
pico_enable_stdio_usb(pico2-cmsis-test 1)

# Add the CMSIS-DSP includes
target_include_directories(pico2-cmsis-test PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
        lib/CMSIS/CMSIS-DSP/Include
)

# Add the standard library to the build
target_link_libraries(pico2-cmsis-test
        pico_stdlib
        arm_cortexM33_math # CMSIS-DSP library for RP2350 (Cortex-M33)
)

pico_add_extra_outputs(pico2-cmsis-test)
