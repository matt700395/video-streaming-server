# you should download requirements
# @ brew install protobuf
# @ brew install opencv
# @ brew install boost
# @ brew install abseil
# @ brew install gRPC
# @ brew install re2
python -m grpc_tools.protoc -I=./ --python_out=./ --grpc_python_out=./ ./stream_service.proto
