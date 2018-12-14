# Lab 3 - CSE 3461
# UDP Socket Programming -- Server

import socket
import os
import sys
import hashlib
from time import sleep

# const variables
directory = "recv"
HEADER_LEN = 8
BLOCKSIZE = 1000 - HEADER_LEN
HOST = ''
PAD = ' '
SIZE_LEN = 4
NAME_LEN = 20

def extractPayload(data):
    ip = socket.inet_ntoa(data[0:4])
    port = str(int.from_bytes(data[4:6], 'big'))
    flag = int.from_bytes(data[6:7], 'little')
    seqNum = int.from_bytes(data[7:8], 'little')
    return ip, port, flag, seqNum, data[8:]

def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def recvFileContentAndWrite(localPORT, trollPort, skt):
    receivedFileSize = 0
    receivedFileSize = False
    receivedFileName = False
    leftFileSize = 1
    expected_Seq_Num = 0 # ACK
    try: 
        while leftFileSize > 0:
            # Receive Data
            oriData, addr = skt.recvfrom(1000)
            if oriData == b'':
                print("No more data")
                break
            # Extract Info
            ip, port, flag, seqNum, data = extractPayload(oriData)
            if seqNum == expected_Seq_Num:
                # Send ACK
                skt.sendto(bytes([seqNum]), (HOST, trollPort))
                if expected_Seq_Num == 0:
                    expected_Seq_Num = 1
                else:
                    expected_Seq_Num = 0
                sleep(0.001)
                # Process data with corresponding flag
                if flag == 1 and not receivedFileSize: # receive size
                    receivedFileSize = True
                    fileSize = int.from_bytes(data,'big')
                    leftFileSize = fileSize
                    print ('Received Filesize: ', fileSize)  
                elif flag == 2 and not receivedFileName: # receive the file name
                    receivedFileName = True
                    fileName = data.decode(encoding='ascii').strip(PAD)
                    print ('Received Filename: ', fileName)
                    # create output file
                    output_file = open('recv/' + fileName, 'wb')
                elif flag == 3: # receive data seg
                    leftFileSize -= len(data)
                    # write each data seg
                    output_file.write(data)
                    print ('Received Data Seg: ', str(fileSize - leftFileSize) + "/"+ str(fileSize))
            else: # Send ACK Again
                skt.sendto(bytes([seqNum]), (HOST, trollPort))
        output_file.close()
        print ('Finish receiving --- Filename: ', fileName, ' Filesize: ', fileSize)  
        # check Md5sum and Diff
        Md5sumAndDiffCheck(fileName)
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
    # open file
    newFile = open("recv/"+fileName, "rb")
    originalFile = open(fileName, 'rb')
    # check
    md5sumCheck(originalFile, newFile)
    diffCheck(originalFile, newFile)
    # close file
    originalFile.close()
    newFile.close()

if __name__ == '__main__':    
    # get parameters 
    localPORT = sys.argv[1]   # local-port-on-System-2 
    trollPort = sys.argv[2]  # troll-port-on-System-2
    
    # create directory
    createDirectory(directory)
    
    # create socket
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # bind the socket to address
    skt.bind((HOST, int(localPORT)))
    
    print ('Socket is open. Waiting for packets...')
    
    # receive file content and write
    recvFileContentAndWrite(int(localPORT), int(trollPort), skt)

    # close socket
    skt.close()