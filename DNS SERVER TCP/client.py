import sys
from socket import *

def main():
	while 1:
		host = "localhost" 
		port = 5000 
		try:
			cSock = socket(AF_INET, SOCK_STREAM)
		except error as msg:
			cSock = None

		try:
			cSock.connect((host, port))
		except error as msg:
			cSock = None 

		if cSock is None:
			print("Error: cannot open socket")
			sys.exit(1) 
		print("Type in a domain name to query, or 'q' to quit:")
		while 1:
			st = input() 
			if st == "":
				continue
			else:
				break
		if st == "q" or  st == "Q":
			cSock.close()
			sys.exit(1) 
		cSock.send(st.encode()) 
		data = cSock.recv(1024).decode() 
		print("Received:", data) 

main()
