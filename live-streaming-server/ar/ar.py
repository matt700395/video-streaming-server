import cv2

cap = cv2.VideoCapture(0)  # Use the default webcam

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform edge detection using the Canny edge detector
    edges = cv2.Canny(gray, 100, 200)

    # Find contours in the edge map
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # Display the resulting frame
    cv2.imshow('Road detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
