import socket
import os
import time

#Establishing connection
s = socket.socket()
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.getfqdn())
# host = socket.gethostname()
port = 9080
print(host)
s.bind((host,port))
s.listen()

clientsocket, address = s.accept()
print(f"Connected with {address}")

listOfFiles = []
listOfFiles.append("/home/vyas20/OS/lab3/B18CSE020/readme.txt")
# listOfFiles.append("/home/vyas20/Pictures/1.png")
listOfFiles.append("/home/vyas20/Pictures/2.png")
listOfFiles.append("/home/vyas20/Downloads/bb.mkv")


print(f"Starting file transferring")

clientsocket.send((str(len(listOfFiles))).encode())
temp = clientsocket.recv(1024).decode()


for file in listOfFiles :
    if(os.path.isfile(file)):
        fileNames = file.split("/")
        fileName = fileNames[len(fileNames)-1]
        print(f"Transferring file {file}")

        clientsocket.send((fileName).encode())        
        temp = clientsocket.recv(1024).decode()

        # f = open(file , 'rb')
        # file_data = f.read(10241024)
        # while(file_data):
        #     clientsocket.send(file_data)
        #     file_data = f.read(10241024)
        #     print(file_data)

        # clientsocket.send((str("Single File Send Terminated !!")).encode())
        # f.close()


        f = open(file , 'rb')
        file_data = f.read(1024102424)
        clientsocket.send(file_data)
        f.close()



        print(f"File {file} successfully transferred")

print(f"File transferring completed !! ")