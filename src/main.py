import os
import sys
import time
import signal
import threading

from gateway.gateway import Gateway as Gateway
from historian.historian import Historian as Historian

def main():
    gw = Gateway()
    hist = Historian()

    gateway = threading.Thread(target=gw.up_server)
    historian_gateway = threading.Thread(target=hist.up_server)
    historian_server_app = threading.Thread(target=hist.up_server_app)
    
    gateway.start()
    historian_gateway.start()
    historian_server_app.start()

    gateway.join()
    historian_gateway.join()
    historian_server_app.join()

    return 0


if __name__ == "__main__":
    sys.exit(main())