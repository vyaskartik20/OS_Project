import socket
import os

directory = []
directory.append("/home/vyas20/OS/lab3/B18CSE020/readme.txt")
directory.append("/home/vyas20/Pictures/1.png")
directory.append("/home/vyas20/Pictures/3.png")
directory.append("/home/vyas20/Pictures/4.png")
directory.append("/home/vyas20/Pictures/2.png")
# directory.append("/home/vyas20/Downloads/bb.mkv")


serversock = socket.socket()
host = socket.gethostbyname(socket.gethostname())
print(f"Enter the address at the other machine : {host}")
port = 9002
serversock.bind((host,port))
filename = ""
serversock.listen(10)
print ("Waiting for the connection.....")

clientsocket,addr = serversock.accept()
print("Got a connection from %s" % str(addr))

password = clientsocket.recv(100).decode()

if(password == "project") :
    print("Authentication with the other machine successful")

    clientsocket.send(str("Y").encode())

    print(f"Initiating file transferring")

    for files in directory:
        print(f"Transferring file {files}")

        fileNames = files.split("/")
        filename = fileNames[len(fileNames)-1]

        size = len(filename)
        size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
        clientsocket.send(size.encode())
        clientsocket.send(filename.encode())

        # filename = os.path.join(path,filename)
        filesize = os.path.getsize(files)
        filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
        clientsocket.send(filesize.encode())
        

        file_to_send = open(files, 'rb')

        l = file_to_send.read()
        clientsocket.sendall(l)
        file_to_send.close()
        print(f"File {files} successfully transferred")

else:
    print("Authentication with the other machine failed")
    clientsocket.send(str("N").encode())


serversock.close()
print()
