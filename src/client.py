import time
import signal
import socket
import struct
import random
import calendar
import threading

from utils.utils import Constants

class Clients:
    def __init__(self, num_clients):
        self.clients = []
        for i in range(num_clients):
            self.clients.append(
                threading.Thread(name='send_position_messages', 
                    target=self.send_position))

    def configure_alarm(self, interval_time):
        signal.signal(signal.SIGALRM, self.send_messages)
        signal.alarm(interval_time)

    def send_messages(self):
        for client in self.clients:
            client.start()
        
        for client in self.clients:
            client.join()
        return
  
    def send_position(self):
        gw_pos_socket = socket.socket(socket.AF_INET, 
                            socket.SOCK_STREAM)
        gw_pos_socket.connect(('127.0.0.1', Constants.GATEWAY_PORT))

        i = 0
        while(i < 50):
            position_list = (
                random.randint(1,10),
                calendar.timegm(time.gmtime()),
                random.uniform(100, 300),
                random.uniform(100, 300),
                random.randint(40,160))
            # position_t = struct.pack('ilffi', position_list)
            
            position = Clients.__format_position_query_string__(position_list)
            http_request = Clients.__format_http_get__(position)
            gw_pos_socket.send(http_request.encode())
            
            print(gw_pos_socket.recv(1024).decode())
            time.sleep(1)
            i = i + 1
        
        gw_pos_socket.close()
        return
            
    @staticmethod
    def __format_position_query_string__(position_list):
        return "id={}&timestamp={}&lat={}&lon={}&speed={}&bearing={}&altitude={}&batt={}".format(
                position_list[0],
                position_list[1],
                position_list[2],
                position_list[3],
                position_list[4],
                random.randint(1,100), random.randint(1,100), 100 * random.random())

    @staticmethod
    def __format_http_get__(position_qry):
        user_agent = 'Python / 3.5.3 Hour of Code DTI Digital / PUC Minas'
        return "POST /?{} HTTP/1.1\r\n".format(position_qry) + \
                "User-Agent: {}\r\n".format(user_agent) + \
                "Host: {}:{}\r\n".format(Constants.GATEWAY_HOST, Constants.GATEWAY_PORT) + \
                "Connection: Keep-Alive\r\n" + \
                "Accept-Encoding: gzip\r\n\r\n"

if __name__ == "__main__":
    clients = Clients(1)
    clients.send_messages()