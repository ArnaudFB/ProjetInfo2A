import sqlite3
from sqlite3 import Error
from utils.Singleton import Singleton

class Database(metaclass=Singleton):  
    
    def __init__(self, db_file:str = "project_database.db"):
        self.__connection = sqlite3.connect(db_file)
    
    # Create connection to the main DB
    def getConnection(self):
        return self.__connection

    def initializeTables():
        # Create the Station table
        initialize_station_request = """CREATE TABLE IF NOT EXISTS Station (
            uuid INT PRIMARY KEY,
            arrondissement INT,
            nom TEXT,
            nbvelo INT,
            lon NUMERIC(10, 6),
            lat NUMERIC(10, 6)
        );"""

        # Create the Date table
        initialize_date_request = """CREATE TABLE IF NOT EXISTS Date (
            uuid INT PRIMARY KEY AUTO INCREMENT,
            date_minute DATETIME
        );"""

        # Create the Record table
        initialize_record_request = """CREATE TABLE IF NOT EXISTS Record (
            station_uuid INT,
            date_uuid INT,
            variation INT,
            FOREIGN KEY (station_id) REFERENCES Station(id),
            FOREIGN KEY (date_id) REFERENCES Date(id)
        );"""

        # Create cursor to execute SQL commands
        conn = self.getConnection()
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
    
    
    def fillTables(data):
        
        data_station = data
        
        for records in data_station:
            station_id=records['stationcode']
            station_name=records['name']
            lat=float((records['coordonnees_geo']['lat']))
            lon=float((records['coordonnees_geo']['lon']))
            nbvelo=records['numbikesavailable']
            new_record={
                'station': {
                    'name':station_name,
                    'uuid':station_id,
                    'latitude':lat,
                    'longitude':lon,
                    },
                }
            station = Station({**new_record})