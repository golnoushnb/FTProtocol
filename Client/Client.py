from socket import *
import os

# serverName = '127.0.0.1'
# serverPort = 2121
serverName = '5.tcp.eu.ngrok.io'
serverPort = 18154

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))



def Help():
    print("\nCall on of the following functions:\n"
          "help             : show this help\n"
          "list             : list files\n"
          "pwd              : show current directory\n"
          "cd dir_name      : change directory\n"
          "dwld filename    : download file\n"
          "quit             : exit\n")

def ls(arg):
    print("Requesting files...\n")
    clientSocket.send(str(arg).encode())
    msg = clientSocket.recv(1024)
    print(msg.decode())

def pwd(arg):
    clientSocket.send(str(arg).encode())
    msg = clientSocket.recv(1024)
    print(msg.decode())

def cd(arg):
    print("changing directory to " + arg[3:])
    clientSocket.send(str(arg).encode())
    msg = clientSocket.recv(1024)
    print(msg.decode())

def dwld(arg):
    dwld_port = clientSocket.recv(1024).decode()
    if dwld_port == 'No such a file':
        print("No such a file")
    else:
        dwld_client_connection = socket(AF_INET, SOCK_STREAM)
        dwld_client_connection.connect((serverName, int(dwld_port)))
        file = arg[5:]
        with open(file, 'wb') as f:
            while True:
                data = dwld_client_connection.recv(1024)
                if data:
                    f.write(data)
                else:
                    print("Successfully downloaded " + file)
                    f.close()
                    dwld_client_connection.close()
                    break

def Quit(arg):
    clientSocket.send(str(arg).encode())
    clientSocket.close()

print('Welcome to the FTP client\n')
Help()

while True:
    arg = input("Enter a command: ")
    if arg == 'help':
        Help()

    elif arg == 'list':
        ls(arg)

    elif arg == 'pwd':
        pwd(arg)

    elif arg.startswith('cd'):
        cd(arg)

    elif arg.startswith('dwld'):
        clientSocket.send(arg.encode())
        dwld(arg)

    elif arg == 'quit':
        Quit(arg)
        break

    else:
        print("command not found !!\n")
