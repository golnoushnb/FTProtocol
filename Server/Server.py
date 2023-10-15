import os
from socket import *
import random

serverName = '127.0.0.1'
serverPort = 2121

server = socket(AF_INET, SOCK_STREAM)
server.bind((serverName, serverPort))
server.listen()
clientConnection, clientAddress = server.accept()

os.chdir('root')
rootPath = os.getcwd()
print(rootPath)

def ls():
    file_size = 0
    file_list = os.listdir()
    msg = ''
    for f in file_list:
        file_size += os.path.getsize(f)
        if os.path.isdir(f):
            msg += '>   ' + f + '     ' + str(os.path.getsize(f)) + 'b' + '\n'
        else:
            msg += '  ' + f + '     ' + str(os.path.getsize(f)) + 'b' + '\n'

    msg += 'Total directory Size : ' + str(file_size) + 'b'
    clientConnection.send(str(msg).encode())

def dwld(file):
    if file in os.listdir() :
        port = random.randint(3000, 50000)
        dwld_socket = socket(AF_INET, SOCK_STREAM)
        dwld_socket.bind((serverName, port))
        dwld_socket.listen()
        clientConnection.send(str(port).encode())
        dwld_connection, dwld_port = dwld_socket.accept()
        with open(file, 'rb') as f:
            dwld_connection.send(f.read())
            f.close()
            dwld_socket.close()
    else:
        print('BAD REQUEST')
        msg = 'No such a file'
        clientConnection.send(str(msg).encode())


def pwd():
    path = os.getcwd()
    if path == rootPath:
        path = '/'
    else:
        path = path[len(rootPath):]
    clientConnection.send(str(path).encode())

def cd(path):
    if os.path.exists(path):
        last_dir = os.getcwd()
        os.chdir(path)
        if os.getcwd().startswith(rootPath):
            msg = 'Directory successfully changed'
        else:
            msg = 'Access Denied!'
            os.chdir(last_dir)
    else:
        msg = 'No such a file'

    clientConnection.send(str(msg).encode())
    print(msg)


print('Welcome to the FTP server\n')

while True:
    print("waiting for instruction")
    req = clientConnection.recv(1024).decode()

    if req == 'help':
        print('Received instruction is: Help')
        pass

    elif req == 'list':
        print('Received instruction is: List')
        ls()

    elif req.startswith('dwld'):
        print('Received instruction is: DWLD')
        dwld(req[5:])

    elif req == 'pwd':
        print('Received instruction is: PWD')
        pwd()

    elif req.startswith('cd'):
        print('Received instruction is: CD')
        cd(req[3:])

    elif req == 'quit':
        print('Received instruction is: QUIT')
        clientConnection.close()
        break

    else:
        print("command not found")