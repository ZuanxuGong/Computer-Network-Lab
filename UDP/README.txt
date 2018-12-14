CSE 5461 Lab 3
Zuanxu Gong (Gong.366@osu.edu)
Original date of Submission: Oct.17th

# Requirements
Python3

# Objective
Write a file transfer application using UDP sockets in Python. The file-transfer protocol will include a server called ftps.py and a client called ftpc.py. ftpc.py will run on one stdlinux computer system that I’ll call System-1; ftps.py will run on another different stdlinux system that I’ll call System-2.

# Machines
System1:
>>hostname
cse-epsilon.coeit.osu.edu
>>/sbin/ifconfig | grep 'inet 164'
inet 164.107.113.21  netmask 255.255.255.0  broadcast 164.107.113.255

System2(My own computer):
>>hostname
Zuanxus-MacBook-Pro.local
>>/sbin/ifconfig | grep 'inet 164'
inet 164.107.161.135 --> 164.107.161.135 netmask 0xffffffff

# Usage
(Under Lab3 directory)
On System2 (My own computer)
1. 
>> python3 ftps.py port
eg:python3 ftps.py 1026

On System 1 (cse-epsilon.coeit.osu.edu)
2. 
>> ./testtroll/troll -C <IP-address-of-System-1> -S <IP-address-of-System-2> -a <client-port-on-System-1> -b <server-port-on-System-2> -r -s 1 -t -x 0 <troll-port-on-System-1>

PS: <client-port-on-System-1> must be set to 1111
eg:./testtroll/troll -C 127.0.0.1 -S 164.107.161.135 -a 1111 -b 1026 -r -s 1 -t -x 0 1234

>> python3 ftpc.py <IP-address-of-System-1> <remote-port-on-System-2> <troll-port-on-System-1> <local-file-to-transfer>

eg: python3 ftpc.py 127.0.0.1 1026 1234 img1.jpg

# Design
1. Simple protocol
   The file transfer application will use a simple protocol. The payload of each UDP segment will contain the remote IP (4 bytes), remote port (2 bytes), and a flag (1 byte), followed by a data/control field as explained below. The flag takes 3 possible values depending on the data/control field.

2. Block of bytes
   Choose 1000 bytes

3. Check whether the transferred file is bitwise identical to the original one
   Use both md5sum and diff
   If indentical, show "The transferred file is bitwise identical to the original one: True"
   Otherwise, show "The transferred file is bitwise identical to the original one: False"

# Sample Output
Socket is open. Waiting for packets...
Finish receiving --- Filename:  img1.jpg  Filesize:  392399
Start checking md5sum for these two files...
(Md5sum checking result) The transferred file is bitwise identical to the original one: True
Start checking diff for these two files...
(Diff checking result) The transferred file is bitwise identical to the original one: True