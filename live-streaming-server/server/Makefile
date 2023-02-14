CC = clang++ -std=c++11 -g3
CFLAGS = -Wall -I/opt/homebrew/opt/opencv/include/opencv4 -I/opt/homebrew/opt/boost/include
LDFLAGS = -L/opt/homebrew/opt/opencv/lib -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -lopencv_videoio -lopencv_core

all: server.cpp
	$(CC) $(CFLAGS) server.cpp $(LDFLAGS) -o server

clean:
	rm -f server
