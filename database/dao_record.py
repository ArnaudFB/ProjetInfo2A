from utils.singleton import Singleton
from database.init_db import Database
from schema.record import Record
import sqlite3
from datetime import datetime 


class DAORecord(metaclass=Singleton):
    
    def add_new_record(self, record: Record) -> bool:
        
        created = False
            
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlAddStation = """INSERT INTO Record (station_uuid, date_uuid, variation )
                            VALUES (%(station_uuid)s, %(date_uuid)s, %(variation)s)"""
            cursor.execute(sqlAddStation, {"station_uuid": record.getStationUuid,
                                    "date_uuid": record.getDateUuid,
                                    "variation": record.getVariation,
                                    })
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def get_var_bystation_date_existing_station(self, station_uuid: int, date_start : datetime, date_end : datetime) -> list[int]:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetRecord = """SELECT variation FROM Record 
                            INNER JOIN Date on uuid=date_uuid 
                            WHERE (station_uuid = %(station_uuid)s)
                            AND (date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)  """
            cursor.execute(sqlGetRecord, {"station_uuid": station_uuid,
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
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetRecord = """SELECT station_uuid, sum(variation) FROM Record 
                            INNER JOIN Date on uuid=date_uuid 
                            WHERE (date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)
                            GROUP BY station_uuid  """
            cursor.execute(sqlGetRecord, {"date_start": date_start,
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
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetRecord = """SELECT variation FROM Record r
                            INNER JOIN Date d on d.uuid=r.date_uuid
                            INNER JOIN Station s on s.uuid=r.station_uuid 
                            WHERE (s.arrondissement=%(arrondissement)s )
                            AND(date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)  """
            cursor.execute(sqlGetRecord, {"arrondissement": arrondissement, 
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
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetRecord = """SELECT arrondissement, sum(variation) FROM Record r
                            INNER JOIN Date d on d.uuid=r.date_uuid
                            INNER JOIN Station s on s.uuid=r.station_uuid 
                            WHERE (date_minute>= %(date_start)s) 
                            AND (date_minute<= %(date_end)s)
                            GROUP BY arrondissement  """
            cursor.execute(sqlGetRecord, {"date_start": date_start,
                                        "date_end": date_end})
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['arrondissement'],res[r]['sum(variation)']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end}"
