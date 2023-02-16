import grpc
import opencv_pb2
import opencv_pb2_grpc
import numpy as np
import cv2

# Create a channel to connect to the gRPC server
channel = grpc.insecure_channel('localhost:50051')

# Create a stub for the StreamService
stub = opencv_pb2_grpc.StreamServiceStub(channel)

# Create a request for the GetMat method
request = opencv_pb2.GetMatRequest(
    rows=480,
    cols=640,
    elt_type=opencv_pb2.OcvMat.INT8,
    value=128
)

# Call the GetMat method to retrieve the Mat data from the server
response = stub.GetMat(request)

# Convert the received Mat data to a NumPy array
mat_data = np.frombuffer(response.mat.mat_data, dtype=np.int8)
img = np.reshape(mat_data, (response.mat.rows, response.mat.cols))

# Display the image using OpenCV
cv2.imshow('Received image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
