from database.init_db import Database
from utils.singleton import Singleton
from schema.date import Date

class DAODate(metaclass=Singleton):

    def get_all(self, date:Date) -> dict[Date]:

        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetAllDate = """SELECT * FROM Date;"""
            cursor.execute(sqlGetAllDate)
            res=cursor.fetchall()

        return

    def add_new(date_time: str) -> bool:
        created = False
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_add_date = """INSERT INTO Date (date_minute)
                            VALUES (%(date_minute)s)"""
            cursor.execute(sql_add_date, {"name": Date.getDate()})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def get_date_byuuid(self, uuid: int) -> Date:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_date = "SELECT date_minute FROM Date WHERE uuid = %(uuid)s"
            cursor.execute(sql_get_date, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            record = res['date_minute']
            return record
        return f"unable to find a date with UUID = {uuid}"   
    
    def get_uuid_bydate(self, date: Date) -> int:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_uuid = "SELECT uuid FROM Date WHERE date_minute = %(date_minute)s"
            cursor.execute(sql_get_uuid, {"date_minute": date})
            res = cursor.fetchone()
        if res:
            record = res['uuid']
            return record
        return f"Unable to find a UUID with date = {date}"