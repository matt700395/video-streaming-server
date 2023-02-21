set(PROTO_FILES
        "./grpc/stream_service.grpc.pb.cc"
        "./grpc/stream_service.grpc.pb.h"
        "./grpc/stream_service.pb.cc"
        "./grpc/stream_service.pb.h")

set(PROTOBUF_INCLUDE_DIRS "/opt/homebrew/opt/protobuf/include")
set(OPENCV_INCLUDE_DIRS "/opt/homebrew/opt/opencv/include/opencv4")
set(BOOST_INCLUDE_DIRS "/opt/homebrew/opt/boost/include")
set(ABSEIL_INCLUDE_DIRS "/opt/homebrew/opt/abseil/include")
set(gRPC_INCLUDE_DIRS "/opt/homebrew/opt/grpc/include")
set(RE2_INCLUDE_DIRS "/opt/homebrew/opt/re2/include")

set(PROTOBUF_LIB_DIRS "/opt/homebrew/opt/protobuf/lib")
set(OPENCV_LIB_DIRS "/opt/homebrew/opt/opencv/lib")
set(BOOST_LIB_DIRS "/opt/homebrew/opt/boost/lib")
set(ABSEIL_LIB_DIRS "/opt/homebrew/opt/abseil/lib")
set(gRPC_LIB_DIRS "/opt/homebrew/opt/grpc/lib")
set(RE2_LIB_DIRS "/opt/homebrew/opt/re2/lib")


add_executable(camera-client
        camera-client.cpp
        ${PROTO_FILES}
        )

target_include_directories(camera-client PRIVATE
        ${PROTOBUF_INCLUDE_DIRS}
        ${OPENCV_INCLUDE_DIRS}
        ${BOOST_INCLUDE_DIRS}
        ${ABSEIL_INCLUDE_DIRS}
        ${gRPC_INCLUDE_DIRS}
        ${RE2_INCLUDE_DIRS}
        )

target_link_directories(camera-client PRIVATE
        ${PROTOBUF_LIB_DIRS}
        ${OPENCV_LIB_DIRS}
        ${BOOST_LIB_DIRS}
        ${ABSEIL_LIB_DIRS}
        ${gRPC_LIB_DIRS}
        ${RE2_LIB_DIRS}
        )

target_link_libraries(camera-client PRIVATE
        opencv_imgcodecs
        opencv_highgui
        opencv_imgproc
        opencv_videoio
        opencv_core
        protobuf
        grpc++
        grpc
        gpr
        re2
        )
