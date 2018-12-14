CSE 5461 Lab 4
Zuanxu Gong (gong.366@osu.edu)
Original date of Submission: Nov.3rd

# Requirements
Python3.7

# Objective
Extend Lab 3 to provide reliable file delivery using the Alternating Bit Protocol over UDP sockets in Python. Packets will be dropped in both directions using one troll process on each machine. A copy of each transmitted data packet needs to be kept until it is ACKed. Note that as ACKs are not ACKed again, so the ACKs are unreliable. You can use a fixed retransmission timeout value of 50 ms.

# Machines
System1:
ssh -X gong.366@zeta.cse.ohio-state.edu
>>hostname
cse-zeta.coeit.osu.edu
>>/sbin/ifconfig | grep 'inet 164'
inet 164.107.113.22  netmask 255.255.255.0  broadcast 164.107.113.255

System2:
ssh -X gong.366@epsilon.cse.ohio-state.edu
>>hostname
cse-epsilon.coeit.osu.edu
>>/sbin/ifconfig | grep 'inet 164'
inet 164.107.113.21  netmask 255.255.255.0  broadcast 164.107.113.255

# Usage
(Under Lab4 directory)
On System 2 (cse-epsilon.coeit.osu.edu)
Step 1: start the server on System-2
>> python3 ftps.py <local-port-on-System-2> <troll-port-on-System-2>
eg:python3 ftps.py 1026 2345

On System 1 (cse-zeta.coeit.osu.edu)
Step 2: start troll on System-1
>> ./testtroll/troll -C <IP-address-of-System-1> -S <IP-address-of-System-2> -a <client-port-on-System-1> -b <server-port-on-System-2> <troll-port-on-System-1> -t -x <packet-drop-%> 
PS: <client-port-on-System-1> must be set to 1111
eg:./testtroll/troll -C 127.0.0.1 -S 164.107.113.21 -a 1111 -b 1026 1234 -t -x 10

On System 2 (cse-epsilon.coeit.osu.edu)
Step 3: start troll on System-2
>> ./testtroll/troll -C <IP-address-of-System-2> -S <IP-address-of-System-1> -a <server-port-on-System-2> -b <client-port-on-System-1> <troll-port-on-System-2> -t -x <packet-drop-%>
PS: <client-port-on-System-1> must be set to 1111
eg:./testtroll/troll -C 127.0.0.1 -S 164.107.113.22 -a 1026 -b 1111 2345 -t -x 10

On System 1 (cse-zeta.coeit.osu.edu)
Step 4: start the client on System-1
>> python3 ftpc.py <IP-address-of-System-1> <remote-port-on-System-2> <troll-port-on-System-1> <local-file-to-transfer>
eg: python3 ftpc.py 127.0.0.1 1026 1234 img1.jpg

# Design
1. Simple protocol
   The file-transfer application uses a simple protocol. The payload of each UDP segment will contain the remote IP (4 bytes), remote port (2 bytes), a flag (1 byte), a 1-bit sequence number (1 byte) that can take values of 0 or 1, followed by a data/control field. The flag takes three possible values depending on the data/control field.

2. Block of bytes
   Choose 1000 bytes

3. Check whether the transferred file is bitwise identical to the original one
   Use both md5sum and diff
   If indentical, show "The transferred file is bitwise identical to the original one: True"
   Otherwise, show "The transferred file is bitwise identical to the original one: False"

4. Handle receiver drop the last ack
Set max timeout count as 100 (1 timeout == 50 ms, so 100 timeout == 5s)
If client repeats sending last package more than maxTimeoutCnt times, which means server drop last ack in a large probability => stop the client

# Sample Output
On System 2 (cse-epsilon.coeit.osu.edu)
Socket is open. Waiting for packets...
Received Filesize:  179755
Received Filename:  img2.jpg
Finish receiving --- Filename:  img2.jpg  Filesize:  179755
Start checking md5sum for these two files...
(Md5sum checking result) The transferred file is bitwise identical to the original one: True
Start checking diff for these two files...
(Diff checking result) The transferred file is bitwise identical to the original one: True

On System 1 (cse-zeta.coeit.osu.edu)
sent firstSeg -- fileSize: 179755
sent secondSeg -- fileName: img2.jpg
sent data segment