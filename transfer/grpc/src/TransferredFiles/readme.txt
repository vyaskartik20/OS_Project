command to compile : g++ Ass5_B18CSE002.cpp -o a -lpthread -lrt
command to run: ./a BarberCount SofaCount WaitingCapacity
Example: ./a 3 4 20

My solution is free from starvation because I am using queue data structure for waiting of customers which follows first in first out policy , ultimately everyone will get a chance thus preventing startvation

My solution is free from deadlock because there is no inter dependency between resources