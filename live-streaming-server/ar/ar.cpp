#include <opencv2/opencv.hpp>
using namespace cv;

int main()
{
  VideoCapture cap(0); // Use the default webcam
  if (!cap.isOpened()) {
	std::cerr << "Failed to open camera." << std::endl;
	return -1;
  }

  while (true) {
	// Capture frame-by-frame
	Mat frame;
	cap >> frame;

	// Convert the frame to grayscale
	Mat gray;
	cvtColor(frame, gray, COLOR_BGR2GRAY);

	// Apply the opposite of Canny edge detection
	Mat edges;
	Canny(gray, edges, 100, 200);
	Mat binary;
	threshold(gray, binary, 127, 255, THRESH_BINARY_INV);
	edges = binary - edges;

	// Apply morphological opening
	Mat kernel = getStructuringElement(MORPH_RECT, Size(3, 3));
	morphologyEx(edges, edges, MORPH_OPEN, kernel);

	// Find contours in the resulting binary image
	std::vector<std::vector<Point>> contours;
	std::vector<Vec4i> hierarchy;
	findContours(edges, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

	// Select the largest rectangular contour
	Rect max_rect;
	for (const auto& contour : contours) {
	  Rect rect = boundingRect(contour);
	  double aspect_ratio = static_cast<double>(rect.width) / rect.height;
	  if (rect.area() > max_rect.area() && aspect_ratio > 1.0 && aspect_ratio < 4.0) {
		max_rect = rect;
	  }
	}

	// Draw the selected contour on the original frame
	if (max_rect.area() > 0) {
	  rectangle(frame, max_rect, Scalar(0, 255, 0), 3);
	}

	// Display the resulting frame
	imshow("Road detection", frame);

	if (waitKey(1) == 'q') {
	  break;
	}
  }

  cap.release();
  destroyAllWindows();
  return 0;
}
