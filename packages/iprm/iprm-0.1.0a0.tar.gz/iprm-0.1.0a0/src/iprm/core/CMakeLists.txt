cmake_minimum_required(VERSION 3.23)

project(iprm_core
    VERSION
        0.1.0
    LANGUAGES
        C CXX
)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(FetchContent)
FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.13.6
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(iprm_core
    src/bindings.cpp
    src/Object.hpp
    src/Object.cpp
    src/Session.hpp
    src/Session.cpp
    src/TypeFlags.hpp
)

set_target_properties(iprm_core
   PROPERTIES
        OUTPUT_NAME
            core
        RUNTIME_OUTPUT_DIRECTORY
            "${CMAKE_CURRENT_SOURCE_DIR}"
        LIBRARY_OUTPUT_DIRECTORY
            "${CMAKE_CURRENT_SOURCE_DIR}"
        ARCHIVE_OUTPUT_DIRECTORY
            "${CMAKE_CURRENT_SOURCE_DIR}"
)
