# Lab 3 - CSE 3461
# UDP Socket Programming -- Client

import ntpath
import socket
import os
import sys
from time import sleep

# const variables
HEADER_LEN = 7;
BLOCKSIZE = 1000 - HEADER_LEN;
HOST = ''
PAD = ' '
CLIENT_PORT=1111
SIZE_LEN = 4
NAME_LEN = 20

def addPayload(ip,port,flag,data):
    ports = int(port)
    chunk = bytearray(4 + 2 + 1 + len(data))
    chunk[0:4]=socket.inet_aton(ip) # 4 bytes IP
    chunk[4:6]=ports.to_bytes(2,'big') # 2 bytes Port
    chunk[6:7]=bytes([flag]) # 1 byte flag
    chunk[7:]=data
    return chunk

def sendFirstSeg(skt, ADDR, HOST, trollPort, localFile):
    # Get Size in bytes
    fileSize = os.path.getsize(localFile)
    fileSizeInBytes = (fileSize).to_bytes(SIZE_LEN,'big')
    # Send the first segment -- the number of bytes in the file to follow
    firstSeg = addPayload(ADDR, trollPort, 1, fileSizeInBytes)
    skt.sendto(firstSeg, (HOST, trollPort))
    print("sent firstSeg -- fileSize: " + str(fileSize))

def sendSecondSeg(skt, ADDR, HOST, trollPort, localFile):
    # Get file name and padding to 20 bytes
    fileName = ntpath.basename(localFile)
    fileName = fileName[0 : min(NAME_LEN, len(fileName))]
    fileNameAfterPadding = fileName.ljust(NAME_LEN, PAD).encode(encoding='ascii')
    # Send the second segment -- the name of the file
    secondSeg = addPayload(ADDR, trollPort, 2, fileNameAfterPadding)
    skt.sendto(secondSeg, (HOST, trollPort))
    print("sent secondSeg -- fileName: " + str(fileName))

def sendFileContent(skt, ADDR, HOST, trollPort, localFile):        
    with open(localFile,'rb') as file:
        while True:
            data = file.read(BLOCKSIZE)
            if data:
                data_seg = addPayload(ADDR, trollPort, 3, data)
                skt.sendto(data_seg, (HOST, trollPort))
                sleep(0.01)
            else:
                break
    print("sent data segment")

if __name__ == '__main__':
    # get parameters 
    ADDR = sys.argv[1]              # IP-address-of-System-1
    PORT = int(sys.argv[2])         # remote-port-on-System-2
    trollPort = int(sys.argv[3])    # troll-port-on-System-1
    localFile = sys.argv[4]         # local-file-to-transfer
    
    # create socket
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    skt.bind((ADDR,CLIENT_PORT))

    # Send the first segment -- the number of bytes in the file to follow
    sendFirstSeg(skt, ADDR, HOST, trollPort, localFile)
    
    # Send the second segment -- the name of the file
    sendSecondSeg(skt, ADDR, HOST, trollPort, localFile)
    
    # send data Segment
    sendFileContent(skt, ADDR, HOST, trollPort, localFile)

    # close socket
    skt.close()