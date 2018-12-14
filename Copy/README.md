#Objective

Write a program called copy.py in Python that reads a file and creates a copy of it in a sub-directory named recv (on the same system). The program will be executed using the command
```
python3 copy.py <filename>
```
where filename is a file in a local directory that needs to be copied. The program opens the file specified in the command line in binary mode and creates a new file with the same name in the recv directory. In a loop, the program keeps reading the next block of bytes (e.g., 1,000 bytes) from the file and writing it to the new file until all bytes have been read from the file. Finally, the program closes the two files.

No buffer, array, or data structure used should exceed 1,000 bytes in size. You cannot read and keep the entire file in memory as your program should be able to work with files of arbitrary size. Your program needs to work with binary files (e.g., images).
