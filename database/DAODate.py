from database.init_db import Database
from utils.Singleton import Singleton
from data.Date import Date
import sqlite3

class DAODate(metaclass=Singleton):
    
    # Create method to add a new date to the database
    def addNewDate(self, date: Date) -> bool:
        
        created = False
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlAddDate = """INSERT INTO Date (date_minute)
                            VALUES (%(date_minute)s)"""
            cursor.execute(sqlAddDate, {"name": Date.getDate()})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    # Create method to obtain a date based on its UUID
    def getDateByUUID(self, uuid: int) -> Date:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetDate = "SELECT date_minute FROM Date WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetDate, {"uuid": uuid}) 
            res = cursor.fetchone()
        if res:
            record = res['date_minute']
            return record
        return f"unable to find a date with UUID = {uuid}"   
    
    def getUUIDByDate(self, date: Date) -> int:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetUUID = "SELECT uuid FROM Date WHERE date_minute = %(date_minute)s"
            cursor.execute(sqlGetUUID, {"date_minute": date})
            res = cursor.fetchone()
        if res:
            record = res['uuid']
            return record
        return f"Unable to find a UUID with date = {date}"