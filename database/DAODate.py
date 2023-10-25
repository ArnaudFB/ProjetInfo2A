from database.init_db import Database
from utils.Singleton import Singleton
from data.Date import Date
import sqlite3

class DAOStation(metaclass=Singleton):
    
    # Create method to create a new Station in the database
    def addNewDate(self, date: Date) -> bool:
        
        created = False
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlAddDate = """INSERT INTO Date (date_minute)
                            VALUES (%(date_minute)s)"""
            cursor.execute(sqlAddDate, {"name": Date.getDate})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def getDateByUUID(self, uuid: int) -> Date:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetDate = "SELECT date_minute FROM Date WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetDate, {"uuid": uuid}) 
            res = cursor.fetchone()
        if res:
            record = res['record']
            return record
        return f"unable to find a record with UUID = {uuid}"   
    
