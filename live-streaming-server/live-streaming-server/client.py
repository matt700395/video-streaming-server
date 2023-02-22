import os
import sys
import grpc
import numpy as np
import cv2
import keras
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gRPC import stream_service_pb2 as str_pb
from gRPC import stream_service_pb2_grpc as str_pb_grpc

def CE_dice_loss(y_true, y_pred, lamb1=0.2, lamb2=0.8, gamma=1e-6):
    CE = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred)

    y_true_dice = K.flatten(K.one_hot(K.cast(y_true, 'int32'), num_classes=15))
    y_pred_dice = K.flatten(y_pred)

    intersect = K.sum(y_true_dice * y_pred_dice, axis=-1)
    denom = K.sum(y_true_dice * y_true_dice, axis=-1) + K.sum(y_pred_dice * y_pred_dice, axis=-1)

    dice_loss = 1 - K.mean((2. * intersect + gamma) / (denom + gamma))

    return lamb1 * CE + lamb2 * (dice_loss)


def load():
    img_path = 'image_process/galaxy_r.jpeg'
    img_raw = cv2.imread(img_path)
    loaded_model = keras.models.load_model("image_process/model/seg_weights.h5",
                                           custom_objects={"CE_dice_loss": CE_dice_loss})
    return img_raw, loaded_model

def filter_raw(frame, loaded_model, img_raw):
    img = np.expand_dims(frame, 0)
    pred = loaded_model.predict(img)
    pred = [pred > 0]
    pred = np.asarray(pred)

    # Extract the probabilities for the road and non-road classes
    pred_road = pred[0, 0, :, :, 1]
    pred_non_road = pred[0, 0, :, :, 0]

    # Compute the predicted class for each pixel
    pred_class = np.argmax(np.stack([pred_non_road, pred_road], axis=-1), axis=-1)

    # Reshape the result to the expected shape
    pred_class = np.reshape(pred_class, (256, 256, 1))

    # Stack the predicted class with a zero array to get the expected shape of (256, 256, 2)
    pred_class = np.concatenate([1 - pred_class, pred_class], axis=-1)

    pred = np.reshape(pred_class, (256, 256, 2))
    frame = np.reshape(frame, (256, 256, 3))

    brightness_threshold = 180  # brightness threshold for filtering
    for j in range(0, 256, 2):
        for k in range(0, 256, 2):
            # Compute the brightness of the current pixel
            brightness = np.mean(frame[j, k, :])
            if (pred[j, k, 0] == 0) or (brightness > brightness_threshold):
                # Crop the replacement image to match the region to be replaced
                img_reshaped = img_raw[j:j + 2, k:k + 2, :]

                # Replace the pixel with the cropped replacement image
                frame[j:j + 2, k:k + 2, :] = img_reshaped

    # frame = cv2.GaussianBlur(frame, (5, 5), 0)
    cv2.imshow('frame', frame)


print("gRPC version: " +  grpc.__version__)

# Create a channel to connect to the gRPC server
try:
    img_raw, loaded_model = load()
    # Create a gRPC channel and stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = str_pb_grpc.StreamServiceStub(channel)

    # Create a new `GetMatRequest` message with the `status` field set to True
    request = str_pb.GetMatRequest(status=True)

    while True:
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

            # Resize the image to 256x256
            mat = cv2.resize(mat, (256, 256))

            # Display the image in a window named "OpenCV Image"
            filter_raw(mat, loaded_model, img_raw)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

except grpc.RpcError as e:
    print(f"Error occurred: {e}")
