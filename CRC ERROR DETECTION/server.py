from message import Message
import numpy as np
import pickle
import socket
import os
from _thread import start_new_thread
def xor(num1,num2):
    res=[]
    for i in range(1,len(num2)):
        if(num1[i]==num2[i]):
            res.append('0')
        else:
            res.append('1')
    return ''.join(res)
def mod2div(divident, divisor): 
    pick = len(divisor)  
    tmp = divident[0 : pick] 
    while pick < len(divident): 
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick] 
        else:  
            tmp = xor('0'*pick, tmp) + divident[pick] 
        pick += 1 
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
    checkword = tmp 
    return checkword 
def encode_data(data,key):
    length=len(key) 
    appended=data + '0'*(length-1) 
    remainder = mod2div(appended, key) 
    return remainder    
def crc_code(input_message):
    data =(''.join(format(ord(x), 'b') for x in input_message))
    key="1001"
    crc=encode_data(data,key) 
    return crc
def parse_message(matrix,crc):
    inverse_matrix=np.array([[1,0,1],[4,4,3],[-4,-3,-3]])
    orginal_matrix=np.dot(inverse_matrix,matrix)
    orginal_matrix=np.transpose(orginal_matrix)
    orginal_matrix=np.concatenate(orginal_matrix)
    received_message=""
    temp=''
    tempint=0
    for j in orginal_matrix:
        if(j==27):
            received_message+=" "
        else:
            tempint=j-1+65
            temp=chr(tempint)
            received_message+=str(temp)
    lastindex=len(received_message)-1
    ans=lastindex
    for i in range(lastindex,-1,-1):
        if(received_message[i]!=' '):
            ans=i
            break
    received_message=received_message[:(ans+1)]
    crc_received=crc_code(received_message)
    if(crc_received==crc):
        resp="Message_received_succesfully"
        print(received_message)
    else:
        resp="Message not received"
    return resp
Serversocket=socket.socket()
ipadress='127.0.0.1'
portno = 1234
count = 0
try:
    Serversocket.bind((ipadress,portno))
except socket.error as e:
    print(str(e))
print('server is listening')
Serversocket.listen(5)
def multithreadedclient(connection):
    connection.send(str.encode("Hello !!"))
    while True:
        received = connection.recv(2048)
        if not received:
            break
        received_object=pickle.loads(received)
        received_matrix=received_object.send_matrix
        crc=received_object.crc_code
        print(crc)
        response=parse_message(received_matrix,crc)
        connection.send(str.encode(response))
    connection.close()
    print("connection close")
while True:
    Client, address=Serversocket.accept()
    print('Connected to :' + address[0] + ':' + str(address[1]))
    start_new_thread(multithreadedclient,(Client,))
    count+=1
    print('Clients Connected :' + str(count))
Serversocket.close()
