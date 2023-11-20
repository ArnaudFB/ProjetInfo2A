from utils.Singleton import Singleton
from database.init_db import Database
from schema.record import Record
import sqlite3
from datetime import datetime 


class DAORecord(metaclass=Singleton):
    
    def get_all(self, record:Record) -> dict[Record]:

        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetAllRecord = """SELECT * FROM Record;"""
            cursor.execute(sqlGetAllRecord)
            res=cursor.fetchall()

        return

    def add_new(record: Record) -> bool:

        created = False
            
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_add_station = """INSERT INTO Record (station_uuid, date_uuid, variation )
                            VALUES (%(station_uuid)s, %(date_uuid)s, %(variation)s)"""
            cursor.execute(sql_add_station, {"station_uuid": record.get_station_uuid,
                                    "date_uuid": record.get_date_uuid,
                                    "variation": record.get_variation,
                                    })
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def get_var_bystation_date_existing_station(self, station_uuid: int, date_start : datetime, date_end : datetime) -> list[int]:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT variation FROM Record 
                            INNER JOIN Date on uuid=date_uuid 
                            WHERE (station_uuid = %(station_uuid)s)
                            AND (date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)  """
            cursor.execute(sql_get_record, {"station_uuid": station_uuid,
                                        "date_start": date_start,
                                        "date_end": date_end})
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['variation']
                records.append(record)
            return records
        return f"unable to find a record for station {station_uuid} between {date_start} and {date_end}"

    def get_var_groupstation_bydate(self, date_start : datetime, date_end : datetime) -> list[tuple]:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT station_uuid, sum(variation) FROM Record 
                            INNER JOIN Date on uuid=date_uuid 
                            WHERE (date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)
                            GROUP BY station_uuid  """
            cursor.execute(sql_get_record, {"date_start": date_start,
                                        "date_end": date_end})
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['station_uuid'],res[r]['sum(variation)']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end}"

    def get_var_byarr_date(self, arrondissement : int , date_start : datetime, date_end : datetime) -> list[tuple]:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT variation FROM Record r
                            INNER JOIN Date d on d.uuid=r.date_uuid
                            INNER JOIN Station s on s.uuid=r.station_uuid 
                            WHERE (s.arrondissement=%(arrondissement)s )
                            AND(date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)  """
            cursor.execute(sql_get_record, {"arrondissement": arrondissement,
                                        "date_start": date_start,
                                        "date_end": date_end})
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['variation']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end} in arrondissement {arrondissement}"

    def get_var_grouparr_bydate(self, date_start : datetime, date_end : datetime) -> list[tuple]:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT arrondissement, sum(variation) FROM Record r
                            INNER JOIN Date d on d.uuid=r.date_uuid
                            INNER JOIN Station s on s.uuid=r.station_uuid 
                            WHERE (date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)
                            GROUP BY arrondissement  """
            cursor.execute(sql_get_record, {"date_start": date_start,
                                        "date_end": date_end})
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['arrondissement'],res[r]['sum(variation)']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end}"
