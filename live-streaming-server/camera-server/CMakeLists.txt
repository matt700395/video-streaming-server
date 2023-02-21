add_executable(camera-server
        camera-server.cpp)
target_include_directories(camera-server PRIVATE "/opt/homebrew/opt/opencv/include/opencv4" "/opt/homebrew/opt/boost/include")
target_link_directories(camera-server PRIVATE "/opt/homebrew/opt/opencv/lib")
target_link_libraries(camera-server PRIVATE opencv_imgcodecs opencv_highgui opencv_imgproc opencv_videoio opencv_core)
