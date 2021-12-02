from message import Message
import socket
import pickle
import numpy as np
def pad(string_parse):
    newlength=len(string_parse)
    while(newlength%3!=0):
        string_parse.append(27)
        newlength=len(string_parse)
    return string_parse
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
def multiply(input_list):
    message_matrix=[]
    temp=[]
    for i in range(len(input_list)):
        if(i%3==2):
            temp.append(input_list[i])
            message_matrix.append(temp)
            temp=[]
        else:
            temp.append(input_list[i])
    message_matrix=np.array(message_matrix)
    key_matrix=np.array([[-3,-3,-4],[0,1,1],[4,3,4]])
    message_matrix=np.transpose(message_matrix)
    multiplied_matrix=np.dot(key_matrix,message_matrix)
    return multiplied_matrix
send_object=Message([],b'')
clientsocket=socket.socket()
ipaddress='127.0.0.1'
portno=1234
print('waiting for response from server')
try:
    clientsocket.connect((ipaddress,portno))
except socket.error as e:
    print(str(e))
received=clientsocket.recv(1024)
received=received.decode('utf-8')
print(received)
while True:
    message=input()
    print(len(message))
    message=message.upper()
    crc_generated=crc_code(message)
    print(crc_generated)
    string_parse=[]
    temp=0
    flag=0
    for i in range(len(message)):
        if(message[i]==' '):
            string_parse.append(27)
        else:
            if(not (ord(message[i])>=65 and ord(message[i])<=90)):
                print("input is not valid")
                flag=1
                break
            string_parse.append(ord(message[i])-64)
    if(flag==0):
        string_parse=pad(string_parse)
        print(string_parse)
        multiplied_matrix=multiply(string_parse)
        send_object.empty()
        send_object.crc_code=crc_generated
        send_object.send_matrix=multiplied_matrix
        send_object_bytes=pickle.dumps(send_object)
        clientsocket.send(send_object_bytes)
        received=clientsocket.recv(1024)
        received=received.decode('utf-8')
        print(received)
clientsocket.close()
