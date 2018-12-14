CSE 5461 Lab 1
Zuanxu Gong (Gong.366@osu.edu)
Original date of Submission: Aug.29
Date of Updating Readme.txt: Sep.6

# Requirements
Python3

# Objective
Write a program called copy.py in Python that reads a file and creates a copy of it in a sub-directory named recv (on the same system).
The program opens the file specified in the command line in binary mode and creates a new file with the same name in the recv directory. In a loop, the program keeps reading the next block of bytes (e.g., 1,000 bytes) from the file and writing it to the new file until all bytes have been read from the file. Finally, the program closes the two files.

# Usage (I ran it on my own mac instead of stdlinux)
(Under Lab1 directory)
1. >> python3 copy.py <filename>  
eg:python3 copy.py img1.jpg

# Design
1. Block of bytes
   Choose 1000 bytes

2. Check whether the transferred file is bitwise identical to the original one
   Use both md5sum and diff
   If indentical, show "The transferred file is bitwise identical to the original one: True"
   Otherwise, show "The transferred file is bitwise identical to the original one: False"

# Sample Output
Finish copying originalFile to recv/img1.jpg
Start checking md5sum for these two files...
(Md5sum checking result) The transferred file is bitwise identical to the original one: True
Start checking diff for these two files...
(Diff checking result) The transferred file is bitwise identical to the original one: True