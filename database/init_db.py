import sqlite3
from sqlite3 import Error
from datetime import datetime
from utils.singleton import Singleton


class Database(metaclass=Singleton):  
    
    def __init__(self, db_file:str = "project_database.db"):
        self.__db_file = db_file
    
    # Create connection to the main DB
    def get_connection(self):
        return sqlite3.connect(self.__db_file)

    def __enter__(self):
        self.__connection = self.get_connection()
        return self.__connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.__connection.close()

    def initialize_tables(self):
        # Create the Station table
        initialize_station_request = """CREATE TABLE IF NOT EXISTS Station (
            uuid INTEGER PRIMARY KEY,
            arrondissement INTEGER,
            nom TEXT,
            nbvelo INTEGER  ,
            lon NUMERIC(10, 6),
            lat NUMERIC(10, 6)
        );"""

        # Create the Date table
        initialize_date_request = """CREATE TABLE IF NOT EXISTS Date (
            uuid INTEGER PRIMARY KEY AUTOINCREMENT,
            date_minute TEXT
        );"""

        # Create the Record table
        initialize_record_request = """CREATE TABLE IF NOT EXISTS Record (
            station_uuid INTEGER,
            date_uuid INTEGER,
            variation INTEGER,
            FOREIGN KEY(station_uuid) REFERENCES Station(uuid),
            FOREIGN KEY(date_uuid) REFERENCES Date(id)
        );"""

        # Create cursor to execute SQL commands
        conn = self.get_connection()
        cur = conn.cursor()

        # Execute SQL commands to initialize DB and TABLES
        try :
            print ("Creating tables...")
            cur.execute(initialize_station_request)
            cur.execute(initialize_date_request)
            cur.execute(initialize_record_request)
        except Exception as error:
            print ('error', error)
        else:
            print ("Tables created successfully")
        finally:
            print ("Closing Connections ... ")
    