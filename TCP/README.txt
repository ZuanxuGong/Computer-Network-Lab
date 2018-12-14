CSE 5461 Lab 2
Zuanxu Gong (Gong.366@osu.edu)
Original date of Submission: Sep.17th

# Requirements
Python3

# Objective
Write a file transfer application using TCP sockets in Python. The file-transfer protocol will include a server called ftps.py and a client called ftpc.py. ftpc.py will run on one stdlinux computer system that I’ll call System-1; ftps.py will run on another different stdlinux system that I’ll call System-2.

# Machines
System1:
hostname: cse-std8.coeit.osu.edu
inet 164.107.113.67  netmask 255.255.255.0  broadcast 164.107.113.255

System2(My own computer):
hostname: Zuanxus-MacBook-Pro.local
inet 164.107.161.154 --> 164.107.161.154 netmask 0xffffffff 

# Usage
(Under Lab2 directory)
On System2 (My own computer)
1. >> python3 ftps.py port
eg:python3 ftps.py 1026

On System 1 (cse-std8.coeit.osu.edu)
2. >> python3 ftpc.py <remote-IP-on-System-2> <remote-port-on-System-2> <local-file-to-transfer>
eg:python3 ftpc.py 164.107.161.154 1026 img1.jpg

# Design
1. Simple protocol
   The first 4 bytes (in network byte order) will contain the number of bytes in the file to follow. The next 20 bytes will contain the name of the file (assume the name fits in 20 bytes). The rest of the bytes in the TCP stream to follow will contain the data in the file. 

2. Block of bytes
   Choose 1000 bytes

3. Check whether the transferred file is bitwise identical to the original one
   Use both md5sum and diff
   If indentical, show "The transferred file is bitwise identical to the original one: True"
   Otherwise, show "The transferred file is bitwise identical to the original one: False"

# Sample Output
System2(My own computer) puts the received file under the recv directory.
On System2 (My own computer) shows:
Connected by ('164.107.113.67', 45716)
Filesize:  392399
Received filename:  img1.jpg
Start checking md5sum for these two files...
(Md5sum checking result) The transferred file is bitwise identical to the original one: True
Start checking diff for these two files...
(Diff checking result) The transferred file is bitwise identical to the original one: True