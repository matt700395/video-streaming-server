import os
import sys
import grpc
import numpy as np
import cv2
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gRPC import stream_service_pb2 as str_pb
from gRPC import stream_service_pb2_grpc as str_pb_grpc

print("gRPC version: " +  grpc.__version__)
# Create a channel to connect to the gRPC server
try:

    # Create a gRPC channel and stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = str_pb_grpc.StreamServiceStub(channel)

    # Create a new `GetMatRequest` message with the `status` field set to True
    request = str_pb.GetMatRequest(status=True)

    # Iterate over the stream of `GetMatResponse` messages returned by the server
    for response in stub.GetMat(request):
        # Retrieve the `rows`, `cols`, and `elt_type` fields from the `OcvMat` object in the response message
        rows = response.mat.rows
        cols = response.mat.cols
        elt_type = response.mat.elt_type

        # Retrieve the `mat_data` field from the `OcvMat` object in the response message
        mat_data = response.mat.mat_data

        # Create a new OpenCV Mat object from the `mat_data` field
        mat = np.frombuffer(mat_data, dtype=np.uint8).reshape(rows, cols, -1)

        # Display the image in a window named "OpenCV Image"
        cv2.imshow("OpenCV Image", mat)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

except grpc.RpcError as e:
    print(f"Error occurred: {e}")
