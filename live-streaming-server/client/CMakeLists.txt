add_executable(client
        client.cpp)

include_directories("./grpc/grpc/include")
include_directories("./grpc/grpc/third_party/abseil-cpp/")

find_package(Protobuf REQUIRED)

target_include_directories(client PRIVATE "/opt/homebrew/opt/opencv/include/opencv4" "/opt/homebrew/opt/boost/include" ${gRPC_INCLUDE_DIR} ${PROTOBUF_INCLUDE_DIRS})
target_link_directories(client PRIVATE "/opt/homebrew/opt/opencv/lib")
target_link_libraries(client PRIVATE opencv_imgcodecs opencv_highgui opencv_imgproc opencv_videoio opencv_core ${gRPC_LIBRARIES})
