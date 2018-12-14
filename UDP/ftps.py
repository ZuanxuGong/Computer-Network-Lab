# Lab 3 - CSE 3461
# UDP Socket Programming -- Server

import socket
import os
import sys
import hashlib

# const variables
directory = "recv"
HEADER_LEN = 7;
BLOCKSIZE = 1000 - HEADER_LEN;
HOST = ''
PAD = ' '
SIZE_LEN = 4
NAME_LEN = 20

def extractPayload(data):
    ip = socket.inet_ntoa(data[0:4])
    port = str(int.from_bytes(data[4:6], 'big'))
    flag = int.from_bytes(data[6:7], 'little')
    return ip, port, flag, data[7:]

def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def receiveFileSize(skt):
    oriData, addr = skt.recvfrom(HEADER_LEN + SIZE_LEN)
    ip, port, flag, data = extractPayload(oriData)
    fileSize = int.from_bytes(data,'big')
    return fileSize

def receiveFileName(skt):
    oriData,addr = skt.recvfrom(HEADER_LEN + NAME_LEN)
    ip, port, flag, fileNameInBytes = extractPayload(oriData)
    fileName = fileNameInBytes.decode(encoding='ascii').strip(PAD);
    return fileName

def recvFileContentAndWrite(PORT, skt):
    receivedFileSize = 0;
    while True:
        try: 
            # receive size
            fileSize = receiveFileSize(skt)
            # receive the file name
            fileName = receiveFileName(skt)

            path = os.path.join(os.getcwd(), directory)
            output_file = os.path.join(path, fileName)

            leftFileSize = fileSize
            with open(output_file,'wb') as file:
                while leftFileSize > 0:
                    oriData, addr = skt.recvfrom(HEADER_LEN + min(leftFileSize, BLOCKSIZE))
                    if oriData == b'':
                        print("No more data")
                        break
                    ip, port, flag, chunk = extractPayload(oriData)
                    leftFileSize -= len(chunk)
                    file.write(chunk)
            print ('Finish receiving --- Filename: ', fileName, ' Filesize: ', fileSize)      
            Md5sumAndDiffCheck(fileName)
            break   
        except RuntimeError as e:
            print(e)
        
def md5sumCheck(originalFile, newFile):
    print("Start checking md5sum for these two files...")
    originalFileHash = hashlib.md5()
    newFileHash = hashlib.md5()
    while True:
        originalData = originalFile.read(BLOCKSIZE)
        newData = newFile.read(BLOCKSIZE)
        if originalData:
            originalFileHash.update(originalData)
            newFileHash.update(newData)
        else:
            break
    print("(Md5sum checking result) The transferred file is bitwise identical to the original one: " + str(originalFileHash.hexdigest() == newFileHash.hexdigest()))

def diffCheck(originalFile, newFile):
    print("Start checking diff for these two files...")
    originalDataTotal = b''
    newDataTotal = b''
    while True:
        originalData = originalFile.read(BLOCKSIZE)
        newData = newFile.read(BLOCKSIZE)
        if originalData:
            originalDataTotal += originalData
            newDataTotal += newData
        else:
            break
    print("(Diff checking result) The transferred file is bitwise identical to the original one: " + str(originalDataTotal == newDataTotal))

def Md5sumAndDiffCheck(fileName):
    newFile = open("recv/"+fileName, "rb")
    originalFile = open(fileName, 'rb')
    md5sumCheck(originalFile, newFile)
    diffCheck(originalFile, newFile)
    originalFile.close()
    newFile.close()

if __name__ == '__main__':    
    # get parameters 
    PORT = sys.argv[1]   # local-port-on-System-2

    # create directory
    createDirectory(directory)
    
    # create socket
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # bind the socket to address
    skt.bind((HOST, int(PORT)))
    
    print ('Socket is open. Waiting for packets...')
    
    # receive file content and write
    recvFileContentAndWrite(PORT, skt)

    # close socket
    skt.close()