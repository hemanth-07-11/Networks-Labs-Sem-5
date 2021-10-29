#client side
import socket
import sys
import time
import os
import hashlib
import pickle     
recv_host='127.0.0.1'
recv_port=9987

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.settimeout(0.001)

filename='./ip1.txt'

lar_num=1
seq_num=1

fileOpen= open(filename, 'rb')  
length=500
offset=500

data = fileOpen.read(length)    
data_fin_state = False    
timeout=0.01 

while not data_fin_state:

    sndpkt=[]
    sndpkt.append(seq_num)
    sndpkt.append(data)

    md5 = hashlib.md5()
    md5.update(pickle.dumps(sndpkt))
    sndpkt.append(md5.digest())

    pkt = pickle.dumps(sndpkt)

    client.sendto(pkt, (recv_host, recv_port))
    last_ackrecv = time.time()    

    print("Sent data", seq_num,'offset',offset)

    if (not data):  
        data_fin_state = not data_fin_state

    try:
        packet,serverAddress = client.recvfrom(4096)
        recv_pkt = []
        recv_pkt = pickle.loads(packet)
        c=recv_pkt[-1]
        del recv_pkt[-1]
        md5rec = hashlib.md5()
        md5rec.update(pickle.dumps(recv_pkt))
        if c == md5rec.digest():   
            print("Received ack:",recv_pkt[0])
   
            seq_num = seq_num + 1
            offset = offset + length
            data = fileOpen.read(length)

            time_recv = time.time()    
            newRTT=time_recv-last_ackrecv       
            timeout=0.9*timeout+0.1*newRTT
            print('adaptive-timeout:',timeout)
            print('\n')

        else:  
            print("error detected")


    except:
        if (time.time() - last_ackrecv >timeout):
            client.sendto(pkt, (recv_host, recv_port))
            print("Timeout")
            print("resent data", seq_num,'length',offset)

fileOpen.close()
print("connection closed")
client.close()
