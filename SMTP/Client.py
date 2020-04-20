# Andrew UM
# HW4
# COMP431

import re
import sys
from socket import *

# input server name followed by space followed by port #
while True:
    try:
        serverName, serverPort = sys.argv[1:]
        break
    except ValueError:
        print 'You need two values.'
        continue
serverPort = int(serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)
print("Socket Created Successfuly")
clientSocket.connect((serverName, serverPort))

# check for handshake
recv = clientSocket.recv(1024)
if recv[:3] != '220':
    print('Unable to connect to server. Please try again later.')
    clientSocket.close()
    sys.exit()
else:
    print("Connected to SMIP server successfully")
    

# Send HELO command and print server response
heloCommand = 'HELO'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)

if recv1[:3] != '250':
    print('Unable to connect to server. Please try again later.')
    clientSocket.close()
    sys.exit()
else:
    print("HELO successfull")
    
x = 0   
while True: 
    # input Sender email
    while True:
        inputFrom = raw_input('From: ')
        clientSocket.send('MAIL FROM: <' + inputFrom + '>')
        okFrom = clientSocket.recv(1024)
        if okFrom[:3] != "250":
            print 'Please enter a valid email address.'
            continue
        else: break
        
 
    # input email recipients separated by comma and space
    while True:
        if x is 1:
            break
        to = raw_input('To: ')
        toList = to.split(", ")
        
        for tos in toList: 
            clientSocket.send('RCPT TO: <' + tos + '>')
            okTo = clientSocket.recv(1024)
            # helper function to check if valid email
            def toHelper():
                if okTo[:3] != "250":
                    print 'One or more email addresses are invalid. Please re-enter'
                    global x
                    x = 0
                    return
                else: 
                    x = 1 
                    return 
            toHelper()
            if x is 0:
                break
                    
    clientSocket.send('DATA')
    okData = clientSocket.recv(1024)
    if okData[:3] != "354":
        print 'There is an error.'
        
    writeFrom = ('From: ' + inputFrom)
    clientSocket.send(writeFrom)
    clientSocket.recv(1024)
    
    writeTo = ('To: ' + to)
    clientSocket.send(writeTo)
    clientSocket.recv(1024)
        
    readSubject = raw_input('Subject: ')
    clientSocket.send('Subject: ' + readSubject + '\n')
    clientSocket.recv(1024)
        
    sys.stdout.write('Message: ')
        
    # read email msg until "."
    while True:
        readData = raw_input()
        if readData == '':
            readData = '\r'
        clientSocket.sendall(readData)
        okEnd = clientSocket.recv(1024)
        if okEnd[:3] == '250':
            clientSocket.send('QUIT')
            quitMsg = clientSocket.recv(1024)
            if quitMsg[:3] != '221':
                print 'There was an error. Quitting.'
                sys.exit()
            else:
                clientSocket.close()
                exit()
        else:
            continue
       
