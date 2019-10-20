import sys
import socket
import struct

from utils.utils import Constants

class AppServer:
    def __init__(self):
        self.server_app_historian_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = ('127.0.0.1', Constants.HISTORIAN_SERVER_APP_PORT)

    def up_server(self):
        print('Para sair use CTRL+X\n')
        print('Request next client trace')
        msg = input()

        while msg != '\x18':
            imei = msg.split(' ')[0]
            length = msg.split(' ')[1]
            self.send_request_to_historian(int(imei), int(length))
            
            response = self.server_app_historian_fd.recvfrom(Constants.MAX_HISTORICAL_DATA_REPLY_T_SIZE)
            num_elements_position_t = int((len(response[0]) - Constants.INT_SIZE_IN_BYTES) / Constants.POSITION_T_SIZE)
            unpack_string = '!i '
            for i in range(num_elements_position_t):
                unpack_string = unpack_string + Constants.PACK_POSITION_T_STRING + ' '
            
            position_list = struct.unpack(unpack_string, response[0])
            num_samples_available = position_list[0]
            for idx in range(1, num_samples_available + 1):
                print("""
                    IMEI: {}
                    TIMESTAMP: {}
                    LAT: {}
                    LONG: {}
                    SPEED: {}
                """.format(position_list[idx*1], position_list[idx*2], position_list[idx*3], position_list[idx*4], position_list[idx*5]))
            print('Request next client trace')
            msg = input()

        self.server_app_historian_fd.close()

    def send_request_to_historian(self, imei, length):
        self.server_app_historian_fd.sendto(struct.pack('ii', imei, length), self.dest)


if __name__ == "__main__":
    sys.exit(AppServer().up_server())