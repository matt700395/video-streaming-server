cmake_minimum_required(VERSION 3.24)
project(live-streaming-server)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g3")

add_executable(client
        live-streaming-server/client/client.cpp)

add_executable(server
        live-streaming-server/server/server.cpp)

target_include_directories(client PRIVATE "/opt/homebrew/opt/opencv/include/opencv4" "/opt/homebrew/opt/boost/include")
target_include_directories(server PRIVATE "/opt/homebrew/opt/opencv/include/opencv4" "/opt/homebrew/opt/boost/include")
target_link_directories(client PRIVATE "/opt/homebrew/opt/opencv/lib")
target_link_directories(server PRIVATE "/opt/homebrew/opt/opencv/lib")
target_link_libraries(client PRIVATE opencv_imgcodecs opencv_highgui opencv_imgproc opencv_videoio opencv_core)
target_link_libraries(server PRIVATE opencv_imgcodecs opencv_highgui opencv_imgproc opencv_videoio opencv_core)
