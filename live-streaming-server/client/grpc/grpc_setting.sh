wget -c https://github.com/protocolbuffers/protobuf/releases/download/v21.12/protobuf-cpp-3.21.12.tar.gz -O - | tar -xz
protoc -I=./ --cpp_out=./ ./stream_service.proto