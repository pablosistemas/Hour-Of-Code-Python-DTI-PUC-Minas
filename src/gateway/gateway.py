import re
import sys
import time
import socket
import struct
import random
import calendar
import threading

from utils.utils import Constants

class Gateway:
    def __init__(self, HOST = Constants.GATEWAY_HOST, PORT = Constants.GATEWAY_PORT):
        self.host = HOST
        self.port = PORT
        self.app_server = None
        self.threads = []

        # server gateway to incoming client monitor messages
        self.app_server = self.__create_socket__(self.host, 
                self.port, socket.SOCK_STREAM)
        self.historian_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # send fake messages to historian 
        # self.threads.append(threading.Thread(target=self.send_position_to_historian))
        # self.threads[-1].start()
        

    @staticmethod
    def __create_socket__(host, port, sock_type):
        tcp_sock = socket.socket(socket.AF_INET, sock_type)    
        src = (host, port)
        tcp_sock.bind(src)
        return tcp_sock

    def pack_message_to_historian(self, position_list):
        return struct.pack(Constants.PACK_POSITION_T_STRING,
            int(position_list[0]), 
            int(position_list[1]), 
            float(position_list[2]),
            float(position_list[3]),
            int(position_list[4]))

    def fake_message_to_historian(self):
        time.sleep(10)
        while(True):
            position_t = struct.pack(Constants.PACK_POSITION_T_STRING, 
                random.randint(1,10),
                calendar.timegm(time.gmtime()),
                random.uniform(100, 300),
                random.uniform(100, 300),
                random.randint(40,160))

            self.send_position_to_historian(position_t)
            time.sleep(5)

    def send_position_to_historian(self, position_t):
        self.historian_client.sendto(
            position_t, (Constants.GATEWAY_HISTORIAN_HOST, 
                Constants.GATEWAY_HISTORIAN_PORT))


    def parse_client_position_message(self, position_qry):
        match_http_get = r'^GET\s\/\?id=(.+)&timestamp=(\d+)&lat=([\+|-]*\d+\.\d+)&lon=([\+|-]*\d+\.\d+)&speed=(\d+)&bearing=(\d+)&altitude=(\d+)&batt=(\d+\.\d+)\sHTTP\/1\.1\r\nUser\-Agent:\s.+\r\nHost:\s\d+\.\d+\.\d+\.\d+:\d+\r\nConnection:\sKeep\-Alive\r\nAccept\-Encoding:\sgzip\r\n\r\n'
        match_obj = re.match(match_http_get, position_qry)
        return match_obj

    def print_client_messages(self, con, client):
        msg = con.recv(1024) # GET or end of connection
        while msg:
            print (client, msg)
            position_match = self.parse_client_position_message(msg.decode())
            if position_match:
                print (client, position_match)
        
                con.send("HTTP/1.1 200 OK\r\nContent-Length: 0\r\nKeep-Alive: timeout=15,max=100\r\n\r\n".encode())

                self.send_position_to_historian(self.pack_message_to_historian(
                    (position_match.group(1),
                    position_match.group(2),
                    position_match.group(3),
                    position_match.group(4),
                    position_match.group(5))))
    
            msg = con.recv(1024) # GET or end of connection
            

        print ('Finalizando conexao do cliente', client)
        con.close()


    def shutdown_server(self, sig, frame):
        for thread in self.threads:
            thread.join()
        print ("Gateway is getting it out")
        sys.exit(-1)

    def up_server(self):
        self.app_server.listen()
        print("Gateway TCP server up and running")
        while True:
            con, client = self.app_server.accept()
            print ('Connected with', client)
            t = threading.Thread(target=self.print_client_messages, args=(con, client,))
            t.start()
            self.threads.append(t)

    def send_historian_message(self):
        pass