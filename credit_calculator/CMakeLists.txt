cmake_minimum_required(VERSION 3.21)
project(credit_calculator)

set(CMAKE_CXX_STANDARD 14)

add_executable(credit_calculator main.cpp bankUtils.hpp logDebug.hpp)
