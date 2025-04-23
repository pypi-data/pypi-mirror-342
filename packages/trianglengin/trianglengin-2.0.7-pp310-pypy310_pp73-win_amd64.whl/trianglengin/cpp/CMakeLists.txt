
cmake_minimum_required(VERSION 3.14)
project(trianglengin_cpp LANGUAGES CXX)

# Locate Pybind11 using variables passed from setup.py (pybind11_DIR)
find_package(pybind11 CONFIG REQUIRED)

# Sources
set(TRIANGLENGIN_SOURCES
    bindings.cpp
    game_state.cpp
    grid_data.cpp
    grid_logic.cpp
    shape_logic.cpp
    # Add other .cpp files if needed
)

# Build the pybind11 module
pybind11_add_module(trianglengin_cpp MODULE ${TRIANGLENGIN_SOURCES})

# C++17 Standard
target_compile_features(trianglengin_cpp PRIVATE cxx_std_17)

# Include directories (current source dir for headers)
target_include_directories(trianglengin_cpp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Optimisation flags and visibility
if(MSVC)
  target_compile_options(trianglengin_cpp PRIVATE /O2 /W4) # Add warning level
else()
  target_compile_options(trianglengin_cpp PRIVATE -O3 -DNDEBUG -Wall -Wextra -pedantic) # Add warnings
  # Symbol visibility for non-Apple Unix-like systems
  if(NOT APPLE)
    target_compile_options(trianglengin_cpp PRIVATE -fvisibility=hidden)
  endif()
endif()

# Output directory is set via CMAKE_LIBRARY_OUTPUT_DIRECTORY in setup.py

# --- Status Messages ---
message(STATUS "pybind11 Include Dirs: ${pybind11_INCLUDE_DIRS}")
message(STATUS "Building C++ extension for Trianglengin version ${TRIANGLENGIN_VERSION_INFO}")
