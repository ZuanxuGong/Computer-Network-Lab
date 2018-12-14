# The ftpc.py client will send all bytes of that local file.

import socket
import os
import sys

def sendFileName(filename, skt):
    if(len(filename) < 20):
        while len(filename) != 20:
            filename += " "
    elif (len(filename) > 20):
        filename = filename[0:20]
    skt.sendall(filename.encode('ascii'))    

def sendFileContent(blockSize, localFile, skt):
    while True:
        data = localFile.read(blockSize)
        if data:
            skt.sendall(data)
        else:
            break

if __name__ == '__main__':
    # const variables
    blockSize = 1000
    fileSizeInBytes = 4
    
    # get parameters
    HOST = str(sys.argv[1])    # remote-IP-on-System-2
    PORT = int(sys.argv[2])    # remote-port-on-System-2
    localFileName = str(sys.argv[3])    # local-file-to-transfer
    
    # create socket
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to a remote socket at address (HOST, PORT)
    skt.connect((HOST, PORT))
    
    # open local file
    localFile = open(localFileName, 'rb')
    
    # send file size
    fileSize=os.path.getsize(localFileName)
    skt.sendall((fileSize).to_bytes(fileSizeInBytes,'big'))    
    # send file name
    sendFileName(localFileName, skt)
    # send file content
    sendFileContent(blockSize, localFile, skt)

    # close socket and local file
    skt.close()
    localFile.close()