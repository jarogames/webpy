//c++  -Wall --permissive -g  hwserver.cpp -lzmq   -o hwserver
#include "zmq.hpp"
#include <string>
#include <iostream>
#ifndef _WIN32
#include <unistd.h>
#else
#include <windows.h>
 
#define sleep(n)    Sleep(n)
#endif
 
int main () {
    //  Prepare our context and socket
    zmq::context_t context (1);
    zmq::socket_t socket (context, ZMQ_PUB); //ZMQ_REP
    socket.bind ("tcp://*:12005");

    int i=0;
    char text1[1000];
    while (true) {
      i=i+1;
        zmq::message_t request;
 
        usleep(500000);
	
	//printf("i am publisher hwserver\n");
	//sprintf(text1,"{\"time\":\"%05d:%d\"}", i , strlen(text1) );
	sprintf(text1,"{\"time\":\"12:00\"", i  );
	for (int j=0;j<8;j++){
	  sprintf(text1,"%s, \"%d\":{\"Rate\":\"%d\"", text1, j, i+j );
	  sprintf(text1,"%s, \"PileUp\":\"%d\"", text1,  j+100 );
	  sprintf(text1,"%s }", text1  );
	}
	sprintf(text1,"%s }", text1 );
	
        zmq::message_t reply (  strlen(text1) );
        memcpy ((void *) reply.data(), text1, strlen(text1) );
	printf("hwserver  PUB  sending /%s/\n", text1);
        socket.send ( reply );
    }
    return 0;
}
