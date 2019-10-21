class Constants:
    SERVAPP_HISTORIAN = '/var/tmp/historian_serverapp_mmap.txt'
    HISTORIAN_SERVAPP = '/var/tmp/serverapp_historian_mmap.txt'
    CLIENT_HISTORY_DATABASE = 'client_history.db'
    GATEWAY_HISTORIAN_PORT = 5001
    GATEWAY_HISTORIAN_HOST = '127.0.0.1'
    HISTORIAN_SERVER_APP_HOST = '0.0.0.0'
    HISTORIAN_SERVER_APP_PORT = 5002
    GATEWAY_HOST = '0.0.0.0'
    GATEWAY_PORT = 5000
    BUFFER_SIZE = 1024
    MAX_POSITION_SAMPLES = 30

    PACK_POSITION_T_STRING = 'iqffi'
    MAX_HISTORICAL_DATA_REPLY_T_SIZE = 724 # 4 + 30 * (4 + 8 + 4 + 4 + 4)
    POSITION_T_SIZE = 24 # id: 4, timestamp: 8, lat: 4, lon: 4, speed: 4
    INT_SIZE_IN_BYTES = 4
    FLOAT_SIZE_IN_BYTES = 4
    TIME_T_SIZE_IN_BYTES = 8

    NUM_MESSAGES_PER_CLIENT = 50
    NUM_CLIENTS = 1