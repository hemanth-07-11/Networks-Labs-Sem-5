import sys, threading, os, random
from socket import *

def main():
	host = "localhost" 
	serverPort = 5000
	#print("Starting server with --> ", host, ":",serverPort)
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(20)

	monitor = threading.Thread(target=monitorquit, args=[])
	monitor.start()

	while 1:
		connectionSock, addr = serverSocket.accept()
		print(addr)
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		server.start()

def dnsQuery(connectionSock, srcAddress):

	dnsAnswers = ""
	found = False
	cacheFile = "DNS_mapping.txt"
	sentence = connectionSock.recv(1024).decode()
	try:
		dataFile = open(cacheFile, "r")
	except IOError:
		dataFile = open(cacheFile, "w")
	for line in dataFile:

		if sentence in line:
			found = True
			print("found in dataFile")
			dnsAnswers = dnsSelection(line)
	dataFile.close()
	if (not found):
		try:
			dnsAnswers = gethostbyname(sentence)
			print("found by DNS lookup")
			dataFile = open(cacheFile, "a")
			dataFile.write(sentence + ":" + dnsAnswers)
			dataFile.write('\n')
			dataFile.close()
		except IOError:
			print("Invalid URL")
	if (dnsAnswers == ""):
		connectionSock.send("Hostname not found\n".encode())
	else:
		print(dnsAnswers)
		if (found):
			dnsAnswers = "Local DNS:" + sentence + ":" + dnsAnswers
		else:
			dnsAnswers = "Root DNS:" + sentence + ":" + dnsAnswers + '\n'
		connectionSock.send(dnsAnswers.encode())
	connectionSock.close()


def dnsSelection(ipList):
	entries = ipList.split(':')
	if (len(entries) <= 2) :
		return entries[1]
	else :
		return entries[random.randint(1,len(entries)-1)]
def monitorquit():
	while 1:
		sentence = input()
		if sentence == "exit":
			os.kill(os.getpid(),9)

main()
