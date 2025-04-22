cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(auspost)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)


# Set C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Add the source files
set(SOURCES
    auspost.c
)

# Create the shared library as a Python extension
add_library(auspost MODULE ${SOURCES})

# Set output name to match Python's expectations
set_target_properties(auspost PROPERTIES
    PREFIX ""
    OUTPUT_NAME "auspost"
    SUFFIX ".so"
)

# Set compile definitions
target_compile_definitions(auspost PRIVATE
    PY_SSIZE_T_CLEAN
)

# Install the library in the package directory
install(TARGETS auspost
    LIBRARY DESTINATION .
)
