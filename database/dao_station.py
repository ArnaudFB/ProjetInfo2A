from database.init_db import Database
from utils.singleton import Singleton
from schema.station import Station
from schema.location import Location
from database.dao import DAO



class DAOStation(metaclass=Singleton):
    
    # Create method to get all Station in the database
    def get_all(station: Station) -> dict[Station]:
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_all_station = """SELECT * FROM Station;"""
            cursor.execute(sql_get_all_station)
            res = cursor.fetchall()
        
        return res
    
    # Create method to create a new Station in the database
    def add_new(station: Station) -> bool:
        
        created = False
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_add_station = """INSERT INTO Station (uuid, arrondissement, nom, nbvelo, lon, lat)
                            VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql_add_station, (station.get_station_id,
                                    station.get_station_arr,
                                    station.get_station_name,
                                    station.get_station_num_bikes,
                                    station.get_station_lon,
                                    station.get_station_lat,))
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
        
    # Get method to retrieve Station by it's UUID
    def get_station_byuuid(uuid: int):
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_station = "SELECT uuid, nom, nbvelo, lon, lat, arrondissement FROM Station WHERE uuid = ?"
            cursor.execute(sql_get_station, (uuid,))
            res = cursor.fetchone()
        if res:
            station_uuid = res[0]
            station_name = res[1]
            station_nbvelo = res[2]
            station_lon = res[3]
            station_lat = res[4]
            station_loc = Location(**{'lon': station_lon, 'lat': station_lat})
            station = Station(**{'station_uuid':station_uuid,
                                 'station_name':station_name,
                                 'loc':station_loc,
                                 'numbikes':station_nbvelo})
            return station
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station by it's UUID
    def get_station_name_byuuid(uuid: int):
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_station = "SELECT nom FROM Station WHERE uuid = ?"
            cursor.execute(sql_get_station, (uuid,))
            res = cursor.fetchone()
        if res:
            station_name = res['nom']
            return station_name
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station's arrondissement by it's UUID
    def get_station_arr_byuuid(uuid: int):
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_station_arr = "SELECT arrondissement FROM Station WHERE uuid = ?"
            cursor.execute(sql_get_station_arr, (uuid,))
            res = cursor.fetchone()
        if res:
            station_arr = res['arrondissement']
            return station_arr
        return f"unable to find a station arrondissement with UUID = {uuid}"    
    
    # Get method to retrieve Station's location by it's UUID
    def get_station_loc_byuuid(uuid: int):
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_station_loc = "SELECT lon, lat FROM Station WHERE uuid = ?"
            cursor.execute(sql_get_station_loc, (uuid,))
            res = cursor.fetchone()
        if res:
            station_loc = res['lon'], res['lat']
            return station_loc
        return f"unable to find a station arrondissement with UUID = {uuid}" 
    
    # Get method to retrieve Station's bikes available by its UUID
    def get_station_numbikes_byuuid(uuid: int):
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_get_station_num_bikes = "SELECT nbvelo FROM Station WHERE uuid = ?"
            cursor.execute(sql_get_station_num_bikes, (uuid,))
            res = cursor.fetchone()
        if res:
            station_numbikes = res[0]
            return station_numbikes
        return f"unable to find a station's bikes number with UUID = {uuid}" 
    
    
    def update_station(station: Station):
        
        updated = False
        
        with Database().get_connection() as connection:
            cursor = connection.cursor()
            sql_update_station = """UPDATE Station SET nom = ?, 
                                                    arrondissement = ?,
                                                    nbvelo = ?,
                                                    lon = ?,
                                                    lat = ?
                                                    WHERE uuid = ?"""
            cursor.execute(sql_update_station, (station.get_station_name,
                                                station.get_station_arr,
                                                station.get_station_num_bikes,
                                                station.get_station_lon,
                                                station.get_station_lat,
                                                station.get_station_id,))
            res = cursor.fetchone()
        if res:
            return not(updated)
        return updated