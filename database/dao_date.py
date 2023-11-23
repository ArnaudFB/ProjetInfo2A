from database.init_db import Database
from utils.singleton import Singleton
from schema.date import Date
from database.dao import DAO

class DAODate(metaclass=Singleton):

    def get_all(date:Date) -> dict[Date]:

        with Database().getConnection() as connection:
            cursor = connection.cursor()
            sqlGetAllDate = """SELECT * FROM Date;"""
            cursor.execute(sqlGetAllDate)
            res=cursor.fetchall()

        return

    def add_new(date_time: str) -> bool:
        created = False
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_add_date = """INSERT INTO Date (date_minute)
                            VALUES (?)"""
            cursor.execute(sql_add_date, (date_time,))
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def get_date_byuuid(uuid: int) -> Date:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_date = "SELECT date_minute FROM Date WHERE uuid = ?"
            cursor.execute(sql_get_date, (uuid,))
            res = cursor.fetchone()
        if res:
            record = res['date_minute']
            return record
        return f"unable to find a date with UUID = {uuid}"   
    
    def get_uuid_bydate(date: str) -> int:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_uuid = "SELECT uuid FROM Date WHERE date_minute = ?"
            cursor.execute(sql_get_uuid, (date,))
            res = cursor.fetchone()
        if res:
            record = res[0]
            return record
        return f"Unable to find a UUID with date = {date}"