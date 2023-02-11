CC = clang++ -std=c++11 -g3
CFLAGS = -Wall -I/opt/homebrew/opt/opencv/include/opencv4 -I/opt/homebrew/opt/boost/include
LDFLAGS = -L/opt/homebrew/opt/opencv/lib -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -lopencv_videoio -lopencv_core

all: main.cpp
	$(CC) $(CFLAGS) main.cpp $(LDFLAGS) -o main

clean:
	rm -f main
