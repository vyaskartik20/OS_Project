import socket
import os
# import thread

serversock = socket.socket()
host = socket.gethostname();
port = 9001;
serversock.bind((host,port));
filename = ""
serversock.listen(10);
print ("Waiting for a connection.....")

clientsocket,addr = serversock.accept()
print("Got a connection from %s" % str(addr))

path = "blah"

directory = os.listdir(path)
for files in directory:
    print (files)
    filename = files
    size = len(filename)
    size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
    clientsocket.send(size.encode())
    clientsocket.send(filename.encode())

    filename = os.path.join(path,filename)
    filesize = os.path.getsize(filename)
    filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
    clientsocket.send(filesize.encode())
    

    file_to_send = open(filename, 'rb')

    l = file_to_send.read()
    clientsocket.sendall(l)
    file_to_send.close()
    print ('File Sent')

serversock.close()
