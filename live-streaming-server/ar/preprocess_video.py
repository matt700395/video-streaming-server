import cv2

# input video file
input_file = './data/test_file/test_video.mp4'

# output video file
output_file = './data/test_file/test_videos..avi'

# frame rate and image size
fps = 20
image_size = (256, 256)

# create VideoCapture object
cap = cv2.VideoCapture(input_file)

# get the codec used for AVI files
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# create VideoWriter object
out = cv2.VideoWriter(output_file, fourcc, fps, image_size)

# read frames from input file and write to output file
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # resize frame to desired image size
    frame = cv2.resize(frame, image_size)
    # write frame to output file
    out.write(frame)

# release resources
cap.release()
out.release()
