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

	// Perform edge detection using the Canny edge detector
	Mat edges;
	Canny(gray, edges, 100, 200);

	// Find contours in the edge map
	std::vector<std::vector<Point>> contours;
	std::vector<Vec4i> hierarchy;
	findContours(edges, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

	// Draw the contours on the original frame
	drawContours(frame, contours, -1, Scalar(0, 255, 0), 3);

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
