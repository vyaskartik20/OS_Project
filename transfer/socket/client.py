import socket

CLIENT_DIR = "TransferredFiles/"

s = socket.socket()
# host = socket.gethostname()
host = input("Enter the IP of the host server : ")
port = 9002
s.connect((host, port))

password = input("Enter the password to initiate the process : ")
s.send(password.encode())

passwordCheck = s.recv(128).decode()

if(passwordCheck == "Y"):

    print("File receiving initiated")

    while True:
        size = s.recv(16).decode() # Note that you limit your filename length to 255 bytes.
        if not size:
            break
        size = int(size, 2)
        filename = s.recv(size).decode()
        print(f"Receiving file {filename}")
        filesize = s.recv(32).decode()
        filesize = int(filesize, 2)
        filename = CLIENT_DIR + filename
        file_to_write = open(filename, 'wb')
        chunksize = 4096
        while filesize > 0:
            if filesize < chunksize:
                chunksize = filesize
            data = s.recv(chunksize)
            file_to_write.write(data)
            filesize -= len(data)

        file_to_write.close()
        print(f"Received file saved as {filename}")

    print ('All files received successfully')
    s.close()

else :
    print("Wrong Password entered, kindly try again !!! ")


print()