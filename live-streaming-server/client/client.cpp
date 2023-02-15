//
// Created by Alvin Lee on 2023/02/14.
//

#include "opencv2/opencv.hpp"
#include <grpcpp/grpcpp.h>
#include "./grpc/stream_service.pb.h"
#include "./grpc/stream_service.grpc.pb.h"

using namespace cv;

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using opencv::OcvMat;
using opencv::StreamService;

class VideoClient {
 public:
  VideoClient(std::shared_ptr<Channel> channel)
	  : stub_(StreamService::NewStub(channel)) {}

  bool SendStream(const Mat& frame) {
	OcvMat ocvMat;
	ocvMat.set_rows(frame.rows);
	ocvMat.set_cols(frame.cols);
	ocvMat.set_elt_type(frame.type());
	ocvMat.set_elt_size(frame.elemSize());

	// Assign the data to the proto message
	ocvMat.set_mat_data(frame.data, frame.total() * frame.elemSize());

	google::protobuf::Empty empty;

	ClientContext context;
	std::unique_ptr<grpc::ClientReaderWriter<OcvMat, google::protobuf::Empty>> writer(stub_->SendStream(&context));

	writer->Write(ocvMat);
	writer->WritesDone();

	Status status = writer->Finish();

	return status.ok();
  }

 private:
  std::unique_ptr<StreamService::Stub> stub_;
};


int main(int argc, char** argv)
{

  //--------------------------------------------------------
  //networking stuff: socket , connect
  //--------------------------------------------------------
  char*       serverIP;
  int         serverPort;

  if (argc < 3) {
	std::cerr << "Usage: cv_video_cli <serverIP> <serverPort> " << std::endl;
	return -1;
  }

  serverIP   = argv[1];
  serverPort = atoi(argv[2]);

  //----------------------------------------------------------
  //OpenCV Code
  //----------------------------------------------------------

  VideoClient client(grpc::CreateChannel(
	  serverIP + std::string(":") + std::to_string(serverPort),
	  grpc::InsecureChannelCredentials())
  );

  VideoCapture capture;
  capture.open(0); // open the default camera

  if (!capture.isOpened()) {
	std::cerr << "Failed to open camera!" << std::endl;
	return -1;
  }

  namedWindow("CV Video Client", 1);

  while (waitKey(10) != 'q') {

	Mat frame;
	capture >> frame; // get a new frame from camera

	if (frame.empty()) {
	  std::cerr << "Failed to capture frame!" << std::endl;
	  break;
	}

	if (!client.SendStream(frame)) {
	  std::cerr << "Failed to send the frame!" << std::endl;
	  break;
	}

	imshow("CV Video Client", frame);
  }

  return 0;
}
