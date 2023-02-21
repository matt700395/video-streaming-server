import numpy as np
import cv2
import os
from glob import glob
import re
import keras

def read_data(data_folder, h, w):
    image_paths = glob(os.path.join(data_folder, 'image_2', '*.png'))
    label_paths = {
        re.sub(r'_(lane|road)_', '_', os.path.basename(path)): path
        for path in glob(os.path.join(data_folder, 'gt_image_2', '*_road_*.png'))}

    images = []
    gt_images = []
    background_color = np.array([255, 0, 0])

    for i in range(len(image_paths)):
        img = cv2.imread(image_paths[i])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (w, h))

        gt_image_path = label_paths[os.path.basename(image_paths[i])]
        gt_image = cv2.imread(gt_image_path)
        gt_image = cv2.cvtColor(gt_image, cv2.COLOR_BGR2RGB)
        gt_image = cv2.resize(gt_image, (w, h))
        gt_bg = np.all(gt_image == background_color, axis=2)
        gt_bg = gt_bg.reshape(*gt_bg.shape, 1)
        gt_image = np.concatenate((gt_bg, np.invert(gt_bg)), axis=2)

        images.append(img)
        gt_images.append(gt_image)

    images = np.asarray(images)
    gt_images = np.asarray(gt_images)
    return images, gt_images


def read_test(data_path, h, w):
    image_paths = glob(os.path.join(data_path, 'image_2', '*.png'))
    images = []
    for i in range(len(image_paths)):
        img = cv2.imread(image_paths[i])
        img = cv2.resize(img, (w, h))
        images.append(img)

    return np.asarray(images)


# IMG_size = (160, 576)
# IMG_size = (160, 160)
height = 256
width = 256
data_path = 'data/data_road/training'
test_path = 'data/data_road/testing'
image, mask = read_data(data_path, height, width)
x_test = read_test(test_path, height, width)


def CE_dice_loss(y_true, y_pred, lamb1=0.2, lamb2=0.8, gamma=1e-6):
    CE = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred)

    y_true_dice = K.flatten(K.one_hot(K.cast(y_true, 'int32'), num_classes=15))
    y_pred_dice = K.flatten(y_pred)

    intersect = K.sum(y_true_dice * y_pred_dice, axis=-1)
    denom = K.sum(y_true_dice * y_true_dice, axis=-1) + K.sum(y_pred_dice * y_pred_dice, axis=-1)

    dice_loss = 1 - K.mean((2. * intersect + gamma) / (denom + gamma))

    return lamb1 * CE + lamb2 * (dice_loss)


for t in range(10):
    img = x_test[t]
    #   cv2_imshow(img)
    cv2.imwrite(
        'result_img/image{}.jpg'.format(
            t), img)

    img = np.expand_dims(img, 0)
    loaded_model = keras.models.load_model("model/seg_weights.h5",
                                           custom_objects={"CE_dice_loss": CE_dice_loss})

    pred = loaded_model.predict(img)
    pred = [pred > 0]
    pred = np.asarray(pred)

    # print(img.shape, pred.shape, height, width)
    # Extract the probabilities for the road and non-road classes
    pred_road = pred[0, 0, :, :, 1]
    pred_non_road = pred[0, 0, :, :, 0]

    # Compute the predicted class for each pixel
    pred_class = np.argmax(np.stack([pred_non_road, pred_road], axis=-1), axis=-1)

    # Reshape the result to the expected shape
    pred_class = np.reshape(pred_class, (256, 256, 1))

    # Stack the predicted class with a zero array to get the expected shape of (256, 256, 2)
    pred_class = np.concatenate([1 - pred_class, pred_class], axis=-1)

    print(pred_class.shape)
    pred = np.reshape(pred_class, (height, width, 2))
    img = np.reshape(img, (height, width, 3))

    for i in range(height):
        for j in range(width):
            if (pred[i, j, 0] == 0):
                img[i, j, 1] = 200

    #   cv2_imshow(img)
    cv2.imwrite(
        'result_img/image{}_result.jpg'.format(
            t), img)
