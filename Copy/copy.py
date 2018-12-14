import sys
import os
import hashlib

def closeTwoFiles(originalFile, newFile):
    originalFile.close()
    newFile.close()

def createCopyInSubDirectory(filename, subDirectory):
    if not os.path.exists(subDirectory):
        os.makedirs(subDirectory)
    return open("recv/"+filename, "wb")    

def writeFiles(blockSize, originalFile, newfile):
    while True:
        data = originalFile.read(blockSize)
        if data:
            newfile.write(data)
        else:
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

if __name__ == '__main__':
    # const variables
    subDirectory = "recv"
    blockSize = 1000
    
    # Read a file
    filename = str(sys.argv[1])
    originalFile = open(filename, 'rb')
    
    # Create a copy of it in a sub-directory named recv
    newFile = createCopyInSubDirectory(filename, subDirectory);
    
    # Keep reading next block of bytes (1,000 bytes) from the file and writing it to the new file until all bytes have been read from the file. 
    writeFiles(blockSize, originalFile, newFile)
    closeTwoFiles(originalFile, newFile)
    print("Finish copying originalFile to recv/"+filename)
    
    # Md5sum check
    originalFile = open(filename, 'rb')
    newFile = open("recv/"+filename, "rb")
    md5sumCheck(blockSize, originalFile, newFile)
    closeTwoFiles(originalFile, newFile)
    
    # Diff check
    originalFile = open(filename, 'rb')
    newFile = open("recv/"+filename, "rb")
    diffCheck(blockSize, originalFile, newFile)
    closeTwoFiles(originalFile, newFile)    

