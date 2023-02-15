add_executable(client
        ./grpc/stream_service.grpc.pb.cc
        ./grpc/stream_service.grpc.pb.h
        ./grpc/stream_service.pb.cc
        ./grpc/stream_service.pb.h
        client.cpp)

set(gRPC_LIBRARIES "./grpc/grpc/include")
set(gRPC_THIRD_PARTY_LIBRARIES "./grpc/grpc/third_party/abseil-cpp")
set(STREAM_SERVICES_LIBRARIES
        "./grpc/stream_service.grpc.pb.cc"
        "./grpc/stream_service.grpc.pb.h"
        "./grpc/stream_service.pb.cc"
        "./grpc/stream_service.pb.h")
set(OPENSSL_ROOT_DIR "/opt/homebrew/opt/openssl")
#set(ABSL_LIBRARIES
#        "absl::lts_20220623::FormatTime"
#        "absl::lts_20220623::ToTimespec"
#        "absl::lts_20220623::RFC3339_full"
#        "absl::lts_20220623::UnknownError"
#        "absl::lts_20220623::InternalError"
#        "absl::lts_20220623::cord_internal::CordzInfo::MaybeTrackCordImpl"
#        "absl::lts_20220623::hash_internal::MixingHashState"
#        "absl::lts_20220623::time_internal::IDivDuration"
#        "absl::lts_20220623::time_internal::cctz::utc_time_zone()"
#        "absl::lts_20220623::CancelledError"
#        "absl::lts_20220623::random_internal::RandenPool::Fill"
#        "absl::lts_20220623::random_internal::RandenHwAes::Absorb"
#        "absl::lts_20220623::random_internal::RandenHwAes::Generate"
#        "absl::lts_20220623::random_internal::Randen::Randen()")

find_package(Protobuf REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(absl REQUIRED)


target_include_directories(client PRIVATE
        "/opt/homebrew/opt/opencv/include/opencv4"
        "/opt/homebrew/opt/boost/include"
        "/usr/local/include"
        "/usr/local/include/grpc"
        "/usr/local/include/grpc++"
#        ${gRPC_THIRD_PARTY_LIBRARIES}
        ${PROTOBUF_INCLUDE_DIRS}
#        ${STREAM_SERVICES_LIBRARIES}
        ${OPENSSL_INCLUDE_DIR}
        ${Boost_INCLUDE_DIRS})
target_link_directories(client PRIVATE "/opt/homebrew/opt/opencv/lib"
        "/usr/local/lib")
#link_directories(
#        "/usr/local/lib"
#        "/opt/homebrew/opt/opencv/lib"
#)
target_link_libraries(client PRIVATE
        opencv_imgcodecs
        opencv_highgui
        opencv_imgproc
        opencv_videoio
        opencv_core
        grpc++
        grpc
        gpr
        re2
        upb
        ${OPENSSL_LIBRARIES})
