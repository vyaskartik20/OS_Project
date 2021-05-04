import socket
# import thread
# import hashlib

s = socket.socket()
host = socket.gethostname()
port = 9001
s.connect((host, port))


while True:
    size = s.recv(16).decode() # Note that you limit your filename length to 255 bytes.
    if not size:
        break
    size = int(size, 2)
    filename = s.recv(size).decode()
    filesize = s.recv(32).decode()
    filesize = int(filesize, 2)
    filename = "new/" + filename
    file_to_write = open(filename, 'wb')
    chunksize = 4096
    while filesize > 0:
        if filesize < chunksize:
            chunksize = filesize
        data = s.recv(chunksize)
        file_to_write.write(data)
        filesize -= len(data)

    file_to_write.close()
    print ('File received successfully')

s.close()
