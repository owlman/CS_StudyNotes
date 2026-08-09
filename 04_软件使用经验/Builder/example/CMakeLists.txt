cmake_minimum_required(VERSION 3.10)
project(calc C)

# ---- 编译选项 ----
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wall -Wextra)
endif()

# ---- 目标 ----
add_executable(calc
    calc/main.c
    calc/getch.c
    calc/getop.c
    calc/stack.c
)

target_include_directories(calc PRIVATE calc)

# ---- 测试 ----
# 集成 test/run_calc.py 作为 ctest 用例
find_package(Python3 COMPONENTS Interpreter QUIET)

if(Python3_Interpreter_FOUND)
    enable_testing()
    add_test(
        NAME calc_pytest
        COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/test/run_calc.py
    )
else()
    message(STATUS "Python3 not found; skipping calc_pytest test target")
endif()

# ---- 安装 ----
include(GNUInstallDirs)
install(TARGETS calc RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})