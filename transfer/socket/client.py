import socket
import os
import time

CLIENT_DIR = "clientFiles"

#Establishing connection
s = socket.socket()
# host = input("Please enter the hostname of the server : ")
port = 9080
s.connect(("127.0.1.1", port))

numFiles = s.recv(100).decode()
numFiles = int(numFiles)
s.send(str("temp").encode())

      
print("File receiving initiated")
#song transferring to this client from the server endpoint
for i in range(numFiles):
    file = s.recv(1024).decode()
    print(f"Receiving file {file}")
    s.send(str("temp").encode())


    # filename = os.path.join(CLIENT_DIR, file)
    # f = open(filename, 'wb')
    # file_data = s.recv(10241024)
    # while 1:
    #     try :
    #         print(file_data.decode())
    #         print()
    #         print()
    #         print()
    #         print()
    #         if(file_data.decode()) == "Single File Send Terminated !!":
    #             print('yes')
    #             break
    #     except :
    #         print('no')
    #         f.write(file_data)
    #         file_data = s.recv(1024102424)
    
    # f.close()


    filename = os.path.join(CLIENT_DIR, file)
    f = open(filename, 'wb')
    file_data = s.recv(1024102424)
    f.write(file_data)    
    f.close()



    print(f"The file {file} received")

print("Receiving all the required files")