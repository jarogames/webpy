//c++  -Wall --permissive -g  zmq_gregory.cpp -lzmq   -o zmq_gregory
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
    //zmq::message_t request;
    
    usleep(2*500000);
    
    //printf("i am publisher hwserver\n");
    //sprintf(text1,"{\"time\":\"%05d:%d\"}", i , strlen(text1) );
    
    int jmax=8;
    int bmax=2;
    sprintf(text1,"{\"time\":\"12:00\"", i  );
    for (int b=0;b<bmax;b++){
    sprintf(text1,"%s, \"%d\":{", text1, b  );
    for (int j=0;j<jmax;j++){
      sprintf(text1,"%s \"%d\":{\"Rate\":\"%.3f\"", text1, j, 0.1*(i+j) );
      sprintf(text1,"%s, \"PileUp\":\"%.1f\"", text1,  1.0*(j) );
      sprintf(text1,"%s }", text1  );
      if (j<jmax-1){      sprintf(text1,"%s,", text1  );}//i need ,
    }// chan
      sprintf(text1,"%s }", text1  );    
      //if (b<bmax-1){      sprintf(text1,"%s,", text1  );}
  }//board
  // //sprintf(text1,"%s, \"histox\":[1,2,3,4,5,6] ", text1  );
    //  sprintf(text1,"%s, \"histoy\":[3,2,1,0,0,%d] ", text1 , i  );
  sprintf(text1,"%s }", text1 );
  
  zmq::message_t reply (  strlen(text1) );
  memcpy ((void *) reply.data(), text1, strlen(text1) );
  printf("hwserver  PUB  sending \n%s\n\n\n", text1);
  socket.send ( reply );
}
return 0;
}
