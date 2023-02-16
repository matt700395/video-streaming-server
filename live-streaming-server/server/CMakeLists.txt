add_executable(server
        server.cpp)
target_include_directories(server PRIVATE "/opt/homebrew/opt/opencv/include/opencv4" "/opt/homebrew/opt/boost/include")
target_link_directories(server PRIVATE "/opt/homebrew/opt/opencv/lib")
target_link_libraries(server PRIVATE opencv_imgcodecs opencv_highgui opencv_imgproc opencv_videoio opencv_core)
