import cv2

# Set the input and output paths and new resolution
input_path = "galaxy.jpeg"
output_path = "galaxy_r.jpeg"
new_width = 256
new_height = 256

# Load the input image
img = cv2.imread(input_path)

# Resize the image to the new resolution
resized_img = cv2.resize(img, (new_width, new_height))

# Save the resized image to the output path
cv2.imwrite(output_path, resized_img)
