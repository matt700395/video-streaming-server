git clone --recurse-submodules -b v1.50.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
chmod 777 -R grpc
wget -c https://github.com/protocolbuffers/protobuf/releases/download/v21.12/protobuf-cpp-3.21.12.tar.gz -O - | tar -xz
# !! before protoc ... you should do following steps to build !!
# $ cd grpc
# $ mkdir -p cmake/build
# $ cd cmake/build
# $ cmake ../..
# $ make -j4
# $ sudo make install
protoc -I=./ --cpp_out=./ --grpc_out=./ --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./stream_service.proto