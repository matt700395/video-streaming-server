#include <opencv2/opencv.hpp>
#include <iostream>
#include <boost/asio.hpp>

using namespace cv;
using namespace std;
using namespace boost::asio;

int main(int argc, char** argv) {
  VideoCapture cap(0); // 0 is the default camera index

  if (!cap.isOpened()) {
    cout << "Error opening camera" << endl;
    return -1;
  }
  std::cout << cap.isOpened() << std::endl;
  io_service service;
  ip::tcp::socket socket(service);
  ip::tcp::endpoint endpoint(ip::address::from_string("0.0.0.0"), 3000);
  try
  {
    socket.connect(endpoint);
  }
  catch(boost::system::system_error& e)
  {
    cout << "Error connecting to server: " << e.what() << endl;
  }
  Mat frame;
  while (true) {
    cap >> frame;

    if (frame.empty()) {
      cout << "End of video stream" << endl;
      break;
    }

    imshow("Video", frame);
    if (waitKey(30) >= 0) {
      break;
    }

    vector<uchar> buf;
    imencode(".jpg", frame, buf);
    write(socket, buffer(buf));
  }

  return 0;
}
