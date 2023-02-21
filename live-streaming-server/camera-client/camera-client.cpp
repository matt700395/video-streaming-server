#include <grpcpp/grpcpp.h>
#include <opencv2/core.hpp>
#include <opencv2/opencv.hpp>
#include "./grpc/stream_service.grpc.pb.h"
#include "./grpc/stream_service.pb.h"
#include <thread>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using gRPC_stream::GetMatRequest;
using gRPC_stream::GetMatResponse;
using gRPC_stream::StreamService;
using gRPC_stream::OcvMat;

// Global variables for the Mat data and synchronization
cv::Mat g_mat;
std::mutex g_mat_mutex;

// Implementation of the GetMat method
class StreamServiceImpl final : public StreamService::Service {
 public:
  Status GetMat(ServerContext *context, const GetMatRequest *request,
				grpc::ServerWriter<GetMatResponse> *writer) {
	std::cout << "GetMat called " << std::endl;
	bool status = request->status();

	// Lock the mutex before accessing the Mat data
	g_mat_mutex.lock();
	// Create and fill a new Mat object from the Mat data
	cv::Mat mat = g_mat.clone();
	// Unlock the mutex after accessing the Mat data
	g_mat_mutex.unlock();

	// Create an OcvMat message with the Mat data
	GetMatResponse response;
	OcvMat* ocvMat = response.mutable_mat();
	ocvMat->set_rows(mat.rows);
	ocvMat->set_cols(mat.cols);
	ocvMat->set_elt_type(mat.type());
	ocvMat->set_mat_data(mat.data, mat.total() * mat.elemSize());

	// Set the mat field of the response message to the new OcvMat object
	writer->Write(response);

	return Status::OK;
  }

};

// Function to handle the socket communication on a separate thread
void socket_thread(char *serverIP, int serverPort) {
  int sokt;
  struct sockaddr_in serverAddr;
  socklen_t addrLen = sizeof(struct sockaddr_in);

  if ((sokt = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
	std::cerr << "socket() failed" << std::endl;
  }

  serverAddr.sin_family = PF_INET;
  serverAddr.sin_addr.s_addr = inet_addr(serverIP);
  serverAddr.sin_port = htons(serverPort);

  if (connect(sokt, (sockaddr *) &serverAddr, addrLen) < 0) {
	std::cerr << "connect() failed!" << std::endl;
  }

  cv::Mat img;
  img = cv::Mat::zeros(720, 1280, CV_8UC1);
  int imgSize = img.total() * img.elemSize();
  uchar *iptr = img.data;
  int bytes = 0;
  int key;

  //make img continuous
  if (!img.isContinuous()) {
	img = img.clone();
  }

  std::cout << "Image Size:" << imgSize << std::endl;

  while (key != 'q') {
	if ((bytes = recv(sokt, iptr, imgSize, MSG_WAITALL)) == -1) {
	  std::cerr << "recv failed, received bytes = " << bytes << std::endl;
	}

	// Lock the mutex before accessing the Mat data
	g_mat_mutex.lock();

	// Copy the received data to the Mat object
	img.copyTo(g_mat);

	// Unlock the mutex after accessing the Mat data
	g_mat_mutex.unlock();

	if (key = cv::waitKey(10) >= 0) break;
  }

  close(sokt);
}

int main(int argc, char **argv) {
  // Start the socket communication thread
  std::cout << "gRPC version: " << grpc::Version() << std::endl;
  std::thread socket_t(socket_thread, argv[1], atoi(argv[2]));

  // Set up the gRPC camera-server on the main thread
  std::string server_address("0.0.0.0:50051");
  StreamServiceImpl service;
  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());

  // Wait for the gRPC camera-server to shut down
  std::cout << "Server listening on " << server_address << std::endl;
  server->Wait();

  // Wait for the socket communication thread to finish
  socket_t.join();

  return 0;
}