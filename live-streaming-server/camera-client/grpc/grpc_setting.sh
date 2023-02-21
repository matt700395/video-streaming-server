# you should download requirements
# @ brew install protobuf
# @ brew install opencv
# @ brew install boost
# @ brew install abseil
# @ brew install grpc
# @ brew install re2
protoc -I=./ --cpp_out=./ --grpc_out=./ --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./stream_service.proto