import cv2
import numpy as np
import os
from glob import glob
import re
import keras

def CE_dice_loss(y_true, y_pred, lamb1=0.2, lamb2=0.8, gamma=1e-6):
    CE = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred)

    y_true_dice = K.flatten(K.one_hot(K.cast(y_true, 'int32'), num_classes=15))
    y_pred_dice = K.flatten(y_pred)

    intersect = K.sum(y_true_dice * y_pred_dice, axis=-1)
    denom = K.sum(y_true_dice * y_true_dice, axis=-1) + K.sum(y_pred_dice * y_pred_dice, axis=-1)

    dice_loss = 1 - K.mean((2. * intersect + gamma) / (denom + gamma))

    return lamb1 * CE + lamb2 * (dice_loss)

def read_test(video_path, h, w):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (w, h))
        frames.append(frame)
    cap.release()
    return np.asarray(frames)

# set up the video path and segmentation model
video_path = '/Users/alvinlee/Git_Folder/car_info/live-streaming-server/ar/data/test_file/test_videos..avi'
output_path = './result_vid/output.avi'
height = 256
width = 256
loaded_model = keras.models.load_model("model/seg_weights.h5",
                                       custom_objects={"CE_dice_loss": CE_dice_loss})
codec_id = "MJPG" # ID for a video codec.
fourcc = cv2.VideoWriter_fourcc(*codec_id)
out = cv2.VideoWriter(output_path, fourcc=fourcc, fps=20, frameSize=(width, height))

# read frames from the video and perform segmentation
frames = read_test(video_path, height, width)
for i in range(frames.shape[0]):
    frame = frames[i]
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

    pred = np.reshape(pred_class, (height, width, 2))
    frame = np.reshape(frame, (height, width, 3))

    for j in range(height):
        for k in range(width):
            if (pred[j, k, 0] == 0):
                frame[j, k, 1] = 200

    # write the segmented frame to a new video file
    out.write(frame)
out.release()
