from socket import AF_INET, SOCK_STREAM, socket

def get(sock, filename):
    print("Recieved File: "+filename)
    try:
        data = sock.recv(1024).decode("utf-8")
        with open(filename, 'w') as outfile:
            while(data):
                outfile.write(data)
                data = sock.recv(1024).decode("utf-8")
                if "EOF-STOP" in data:
                    stop_point = data.find("EOF-STOP")
                    outfile.write(data[:stop_point])
                    return data[stop_point+8:]
    except Exception as e:
        print(e)
        error_message = "There has been an error recieving the requested file."
        sock.sendall(error_message.encode('utf-8'))

def put(sock, filename):
    try:
        sock.send(" ".encode('utf-8'),1024)
        with open(filename, 'r') as infile:
            for line in infile:
                sock.sendall(line.encode('utf-8'))
        end_message = "EOF-STOP"
        sock.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        error_message = "There has been an error sending the requested file. " + filename + " might not exist"
        sock.sendall(error_message.encode('utf-8'))


command_list = ["QUIT","GET","PUT"]
HOST = '127.0.0.1'
PORT = 5000

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))

while (True):
    s = input("Message: ")
    sock.sendall(s.encode("utf-8"))
    command = s.split(' ')[0].upper()

    if command in command_list:
        if command == "QUIT":
            print("Disconnecting...Bye")
            break
            port = int(s.split(' ')[1])

        if command == "GET":
            filename = s.split(' ')[1]
            remainder = get(sock, filename)

        if command == "PUT":
            filename = s.split(' ')[1]
            put(sock, filename)
            print("File sent to server Successfully")

    else:
        data = sock.recv(1024).decode("utf-8")
        print ("Received: ", data)

sock.close()
