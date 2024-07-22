cmake_minimum_required(VERSION 3.15)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(Apollo LANGUAGES CXX C)

file(GLOB_RECURSE SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)
add_executable(apollo main.cpp ${SOURCE_FILES})

target_include_directories(apollo PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

find_package(PortAudio REQUIRED)
target_link_libraries(apollo PRIVATE portaudio_static)
