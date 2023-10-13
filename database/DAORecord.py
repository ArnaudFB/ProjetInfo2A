from utils.Singleton import Singleton
from database.init_db import Database
from data.Record import Record
import sqlite3

# TODO : Change first method to connect to the correct table and extract expected values

class DAORecord(metaclass=Singleton):
    
    def addNewRecord(self, record: Record) -> bool:
        
        created = False
            
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlAddStation = """INSERT INTO Station (stationid, stationname, lon, lat)
                            VALUES (%(uuid)s, %(name)s, %(lon)s, %(lat)s)"""
            cursor.execute(sqlAddStation, {"uuid": station.getStationID,
                                    "name": station.getStationName,
                                    "lon": station.getStationLon,
                                    "lat": station.getStationLat})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def getRecordByUUID(self, uuid: int) -> Record:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetRecord = "SELECT record FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetRecord, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            record = res['record']
            return record
        return f"unable to find a record with UUID = {uuid}"