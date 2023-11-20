from utils.singleton import Singleton
from database.init_db import Database
from schema.record import Record
from datetime import datetime 


class DAORecord(metaclass=Singleton):
    
    def get_all(record:Record) -> dict[Record]:

        with Database().getConnection() as connection:
            cursor = connection.cursor()
            sqlGetAllRecord = """SELECT * FROM Record;"""
            cursor.execute(sqlGetAllRecord)
            res=cursor.fetchall()

        return

    def add_new(record: Record) -> bool:

        created = False
            
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_add_station = """INSERT INTO Record (station_uuid, date_uuid, variation )
                            VALUES (?, ?, ?)"""
            values=(record.get_station_uuid,
                    record.get_date_uuid,
                    record.get_variation,
                    )
            cursor.execute(sql_add_station, values)
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
    
    def get_var_bystation_date_existing_station(station_uuid: int, date_start : datetime, date_end : datetime) -> list[int]:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT variation FROM Record 
                            INNER JOIN Date on uuid=date_uuid 
                            WHERE (station_uuid = ?)
                            AND (date_minute>= ?) 
                            AND (date_minute<= ?)  """
            values=(station_uuid,
                    date_start,
                    date_end,)
            cursor.execute(sql_get_record, values)
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['variation']
                records.append(record)
            return records
        return f"unable to find a record for station {station_uuid} between {date_start} and {date_end}"

    def get_var_groupstation_bydate(date_start : datetime, date_end : datetime) -> list[tuple]:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT station_uuid, sum(variation) FROM Record 
                            INNER JOIN Date on uuid=date_uuid 
                            WHERE (date_minute>= ?) 
                            AND (date_minute<= ?)
                            GROUP BY station_uuid  """
            cursor.execute(sql_get_record, (date_start, date_end,))
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['station_uuid'],res[r]['sum(variation)']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end}"

    def get_var_byarr_date(arrondissement : int , date_start : datetime, date_end : datetime) -> list[tuple]:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT variation FROM Record r
                            INNER JOIN Date d on d.uuid=r.date_uuid
                            INNER JOIN Station s on s.uuid=r.station_uuid 
                            WHERE (s.arrondissement=? )
                            AND(date_minute>= ?) 
                            AND (date_minute<= ?)  """
            cursor.execute(sql_get_record, (arrondissement,
                                        date_start,
                                        date_end,))
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['variation']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end} in arrondissement {arrondissement}"

    def get_var_grouparr_bydate(date_start : datetime, date_end : datetime) -> list[tuple]:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_record = """SELECT arrondissement, sum(variation) FROM Record r
                            INNER JOIN Date d on d.uuid=r.date_uuid
                            INNER JOIN Station s on s.uuid=r.station_uuid 
                            WHERE (date_minute>= ?) 
                            AND (date_minute<= ?)
                            GROUP BY arrondissement  """
            cursor.execute(sql_get_record, (date_start, date_end,))
            res = cursor.fetchall()
        if res:
            records=[]
            for r in range(len(res)): 
                record = res[r]['arrondissement'],res[r]['sum(variation)']
                records.append(record)
            return records
        return f"unable to find a record between {date_start} and {date_end}"
