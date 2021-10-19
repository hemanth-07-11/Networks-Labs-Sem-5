from socket import AF_INET, SOCK_STREAM, socket

def get(conn, filename):
    try:
        with open(filename, 'r') as infile:
            for line in infile:
                conn.sendall(line.encode('utf-8'))    
        end_message = "EOF-STOP"
        conn.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        error_message = ("There has been an error sending the requested file. "+ filename + " might not exist")
        conn.sendall(error_message.encode('utf-8'))

def put(conn, data):
    filename = data.split(' ')[1]
    print("Recieved File: "+filename)

    try:
        data = conn.recv(1024).decode("utf-8")
        with open(filename, 'w') as outfile:
            while(data):
                outfile.write(data)
                data = conn.recv(1024).decode("utf-8")
                if "EOF-STOP" in data:
                    stop_point = data.find("EOF-STOP")
                    outfile.write(data[:stop_point])
                    return data[stop_point+8:]
    except Exception as e:
        print(e)
        error_message = "There has been an error recieving the requested file."
        conn.sendall(error_message.encode('utf-8'))
        return ""

command_list = ["QUIT","GET","PUT"]

HOST = '127.0.0.1'
PORT = 5000

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))
print("Server is ready to listen")

while True:
    sock.listen()
    conn, addr = sock.accept()
    print("Connected to " , addr)

    remainder = ""
    while (True):
        command = ""
        if remainder == "":
            data = conn.recv(1024).decode("utf-8")
            command = data.split(' ')[0].upper()
        else:
            data = remainder
            space = remainder.find(' ')
            command = remainder[:space].upper()
            remainder = ""

        if command in command_list:
            if command == "QUIT":
                print("Client quitting")
                conn.sendall(command.encode("utf-8"))
                conn.close()
                break
            
            if command == "GET":
                filename = data.split(' ')[1]
                get(conn, filename)

            if command == "PUT":
                remainder = put(conn, data)

        else:
            print(data)
            conn.sendall(data.upper().encode("utf-8"))
    print("Disconnected from:", addr)

sock.close()
