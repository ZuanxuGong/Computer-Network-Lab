# The ftps.py server should receive the file and then store it. 
# Make sure that the new file created by ftps.py is in a different directory to avoid overwriting the original file
# since all CSE machines have your root directory mounted.

import socket
import os
import sys
import hashlib

def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def recvFileContentAndWrite(blockSize, newFile, conn):
    while True:
        data = conn.recv(1000)
        newFile.write(data)
        if not data:
            break
        
def md5sumCheck(blockSize, originalFile, newFile):
    print("Start checking md5sum for these two files...")
    originalFileHash = hashlib.md5()
    newFileHash = hashlib.md5()
    while True:
        originalData = originalFile.read(blockSize)
        newData = newFile.read(blockSize)
        if originalData:
            originalFileHash.update(originalData)
            newFileHash.update(newData)
        else:
            break
    print("(Md5sum checking result) The transferred file is bitwise identical to the original one: " + str(originalFileHash.hexdigest() == newFileHash.hexdigest()))

def diffCheck(blockSize, originalFile, newFile):
    print("Start checking diff for these two files...")
    originalDataTotal = b''
    newDataTotal = b''
    while True:
        originalData = originalFile.read(blockSize)
        newData = newFile.read(blockSize)
        if originalData:
            originalDataTotal += originalData
            newDataTotal += newData
        else:
            break
    print("(Diff checking result) The transferred file is bitwise identical to the original one: " + str(originalDataTotal == newDataTotal))

def Md5sumAndDiffCheck(fileName):
    newFile = open("recv/"+fileName, "rb")
    originalFile = open(fileName, 'rb')
    md5sumCheck(blockSize, originalFile, newFile)
    diffCheck(blockSize, originalFile, newFile)
    originalFile.close()
    newFile.close()

if __name__ == '__main__':
    # const variables
    fileSizeInBytes = 4
    directory = "recv"
    blockSize = 1000
    HOST = ''
    
    # get parameters 
    PORT = int(sys.argv[1])   # local-port-on-System-2
    
    # create directory
    createDirectory(directory)
    
    # create socket
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to address
    skt.bind((HOST, PORT))
    # Enable a server to accept connections. 
    skt.listen(1)
    # accept a connection. conn: a new socket object usable to send and receive data on the connection. address: address bound to the socket on the other end of the connection
    conn, addr = skt.accept()
    print ('Connected by', addr)
    
    # receive file size
    fileSize = conn.recv(fileSizeInBytes)
    size=int.from_bytes(fileSize,'big')
    print("Filesize: ", size)    
    # receive file name
    data = conn.recv(20)
    fileName = data.decode('ascii').strip()
    print("Received filename: ", fileName)
    
    # open file in recv
    newFile = open("recv/" + fileName, "wb")
    
    # receive file content and write
    recvFileContentAndWrite(blockSize, newFile, conn)
    
    # close connection and file
    conn.close()
    newFile.close()
    
    # Md5sum and Diff Check
    Md5sumAndDiffCheck(fileName)