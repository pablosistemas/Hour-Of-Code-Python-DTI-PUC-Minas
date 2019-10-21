import struct
import sqlite3

from utils.utils import Constants

class SQLiteManager:
    def __init__(self, *args, **kwargs):
        self.conn = None
        self.__setup__()

    def __setup__(self):
        self.conn = sqlite3.connect(Constants.CLIENT_HISTORY_DATABASE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS CLIENTS')
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS CLIENTS  (  
            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            IMEI           KEY   NOT NULL,
            TIMESTAMP      TEXT  NOT NULL,
            LATITUDE       TEXT  NOT NULL,
            LONGITUDE      TEXT  NOT NULL,
            SPEED          TEXT  NOT NULL);
        """)
        self.conn.commit()
    
    def insert_position_into_db(self, position_list):
        self.cursor.execute("""
        INSERT INTO CLIENTS (IMEI, TIMESTAMP, LATITUDE, LONGITUDE, SPEED) 
        VALUES ({}, {}, {}, {}, {})
        """.format(position_list[0], 
            position_list[1], position_list[2], position_list[3], position_list[4]))

        self.conn.commit()

    def request_position_by_id(self, id, num_samples):
        self.cursor.execute("""
            SELECT * FROM CLIENTS WHERE IMEI={} ORDER BY ID DESC LIMIT {}
        """.format(id, num_samples))
        position_t_a = []
        pack_string = '!i '
        for history in self.cursor.fetchall():
            position_t_a.append(int(history[1]))
            position_t_a.append(int(history[2]))
            position_t_a.append(float(history[3]))
            position_t_a.append(float(history[4]))
            position_t_a.append(int(history[5]))
            pack_string = pack_string + Constants.PACK_POSITION_T_STRING
        
        if len(position_t_a) > 0:
            historical_data_reply_t = struct.pack(pack_string, int(len(position_t_a) / 5), *position_t_a)
        else:
            historical_data_reply_t = struct.pack(pack_string, 0)
        return historical_data_reply_t