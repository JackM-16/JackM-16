import socket
import time

def client_program():
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect(('127.0.0.1', port))  # connect to the server


    while True:
        data = client_socket.recv(1024).decode()
        print(data)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
