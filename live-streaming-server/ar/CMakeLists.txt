set(OPENCV_INCLUDE_DIRS
        "/opt/homebrew/opt/opencv/include/opencv4"
        )
set(OPENCV_LIB_DIRS "/opt/homebrew/opt/opencv/lib")
add_executable(ar
        ar.cpp
        )
find_package(OpenCV REQUIRED)

target_include_directories(ar PRIVATE
        ${OPENCV_INCLUDE_DIRS}
        )

target_link_directories(ar PRIVATE
        ${OPENCV_LIB_DIRS}
        )

target_link_libraries(ar PRIVATE
        ${OpenCV_LIBS} opencv_aruco
        )