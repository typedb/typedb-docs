cmake_minimum_required(VERSION 3.27)
project(main)

set(CMAKE_CXX_STANDARD 17)
link_directories(${PROJECT_SOURCE_DIR}/lib)
include_directories(${PROJECT_SOURCE_DIR}/include)

add_executable(main main.cpp)
IF (WIN32)
    target_link_libraries(main ${PROJECT_SOURCE_DIR}/lib/typedb-driver-cpp.if.lib)
ELSE()
    target_link_libraries(main typedb-driver-cpp)
ENDIF()
