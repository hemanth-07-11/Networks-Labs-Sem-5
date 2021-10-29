#server side
import socket
import pickle
import hashlib
import sys
import numpy as np
import time

serverIP="127.0.0.1"
serverPort=9987

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((serverIP,serverPort))
server.settimeout(3)
print("Ready to serve")

expected_seqnum=1
ACK=1
ack = []

f = open("output", "wb")
end_of_file = False	
last_pkt_recv = time.time()	
starttime = time.time()

while True:
    try:
        recvpkt=[]

        packet,clientAddress= server.recvfrom(4096)
        recvpkt = pickle.loads(packet)

        c = recvpkt[-1]	
        del recvpkt[-1]    

        md5 = hashlib.md5()
        md5.update(pickle.dumps(recvpkt))
        if c == md5.digest():  
            sndpkt = []
            sndpkt.append(recvpkt[0])
            md5send = hashlib.md5()
            md5send.update(pickle.dumps(sndpkt))
            sndpkt.append(md5send.digest())
            ack_pkt = pickle.dumps(sndpkt)
            server.sendto(ack_pkt, (clientAddress[0], clientAddress[1]))
            print("New Ack", recvpkt[0])
            if (recvpkt[0] == expected_seqnum):    
                print("ACCEPT",recvpkt[0])
                if recvpkt[1]: 
                    f.write(recvpkt[1])
                else: 
                    end_of_file = True

                expected_seqnum = recvpkt[0] + 1  


            else: 
                print('Out of Order')
                print('IGNORED')

        else: 
            print('Error detected')
            print('IGNORED')

    except:
        if end_of_file:  
            if (time.time() - last_pkt_recv > 0.1):
                break

endtime = time.time()
f.close()
print('FILE TRANSFER SUCCESSFUL')
print("TIME TAKEN "), str(endtime - starttime)
