# CSCI 379
# Programming Project 1
# Jacob Feldman

from socket import *
import ServerModule  # My own module
import threading  # For multiple clients.
import Game

port = 9999
clientMax = 1024

sSocket = socket(AF_INET, SOCK_STREAM)  # TCP connection
sSocket.bind(('', port))

print('Starting Pairing service\n')
threading.Thread(target=ServerModule.pairing).start()  # Starting Pairing Service
print('Pairing service started\n')
print('Accepting connections\n')
while True:
    sSocket.listen(1)
    connection, addr = sSocket.accept()
    print 'Client Connected'
    threading.Thread(target=ServerModule.serverclient, args=(connection, addr)).start()  # For multiple clients.
