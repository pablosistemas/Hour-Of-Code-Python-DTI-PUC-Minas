import contextlib
import threading
import socket
import struct

from utils.utils import Constants
from repository.sqlite_manager import SQLiteManager as SQLiteManager

class Historian:
    def __init__(self):
        self.gw_hist_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hist_serverapp_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_app_dst = (Constants.HISTORIAN_SERVER_APP_HOST,
                Constants.HISTORIAN_SERVER_APP_PORT)
        self.sqlite_instance = SQLiteManager()

    def up_server(self):
        self.gw_hist_fd.bind((Constants.GATEWAY_HISTORIAN_HOST, Constants.GATEWAY_HISTORIAN_PORT))
        print("Historian UDP server up and listening")

        while(True):
            bytesAddressPair = self.gw_hist_fd.recvfrom(Constants.BUFFER_SIZE) 
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            unpacked_message = struct.unpack(Constants.PACK_POSITION_T_STRING, message)
            clientMsg = "Message from Client: {}".format(unpacked_message)
            clientIP  = "Client IP Address: {}".format(address)
            print(clientMsg)
            print(clientIP)
            self.__record_database__(unpacked_message)
        
        return
    
    def __record_database__(self, position_list):
        self.sqlite_instance.insert_position_into_db(position_list)

    def __request_database__(self, id, num_samples):
        return self.sqlite_instance.request_position_by_id(id, num_samples)

    def up_server_app(self):
        self.hist_serverapp_fd.bind(self.server_app_dst)
        print("Historian UDP server_app up and listening")
        
        while(True):
            try:
                bytesAddressPair = self.hist_serverapp_fd.recvfrom(Constants.BUFFER_SIZE) 
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]

                historical_data_request_t = struct.unpack('ii', message)
                binary_response = self.__request_database__(int(historical_data_request_t[0]), int(historical_data_request_t[1]))
                self.hist_serverapp_fd.sendto(binary_response, address)
            except Exception as e:
                print(str(e))
                continue