import sys
import socket
import threading

class Gateway:
    def __init__(self, HOST = '0.0.0.0', PORT = 5000):
        self.host = HOST
        self.port = PORT
        self.tcp_sock = None
        self.__create_socket__()
    
    def __create_socket__(self):
        self.tcp_sock = socket.socket(socket.AF_INET, 
            socket.SOCK_STREAM)    
        src = (self.host, self.port)
        self.tcp_sock.bind(src)

    def up_server(self):
        self.tcp_sock.listen()
        print("I am waiting for new clients")
        while True:
            con, client = self.tcp_sock.accept()
            print ('Conectado por', client)
            msg = con.recv(1024)
            while msg:
                print (client, msg)
                msg = con.recv(1024)

            print ('Finalizando conexao do cliente', client)
            con.close()


def main():
    gw = Gateway()
    gw.up_server()

if __name__ == "__main__":
    exit(main())