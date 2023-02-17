cmake_minimum_required(VERSION 3.24)
project(live-streaming-server)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_COMPILER /Library/Developer/CommandLineTools/usr/bin/clang++)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g3")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(client)
add_subdirectory(server)
add_subdirectory(ar)

