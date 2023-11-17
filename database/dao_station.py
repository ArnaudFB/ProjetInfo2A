from database.init_db import Database
from utils.Singleton import Singleton
from schema.station import Station
from schema.location import Location
import sqlite3


class DAOStation(metaclass=Singleton):
    
    # Create method to get all Station in the database
    def get_all_station(self, station: Station) -> dict[Station]:
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_all_station = """SELECT * FROM Station;"""
            cursor.execute(sql_get_all_station)
            res = cursor.fetchall()
        
        return res
    
    # Create method to create a new Station in the database
    def add_new_station(self, station: Station) -> bool:
        
        created = False
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_add_station = """INSERT INTO Station (uuid, arrondissement, nom, nbvelo, lon, lat)
                            VALUES (%(uuid)s,%(arrondissement)s %(name)s, %(nbvelo)s, %(lon)s, %(lat)s)"""
            cursor.execute(sql_add_station, {"uuid": station.get_station_id,
                                    "arrondissement": station.get_station_arr,
                                    "name": station.get_station_name,
                                    "nbvelo": station.get_station_num_bikes,
                                    "lon": station.get_station_lon,
                                    "lat": station.get_station_lat})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
        
    # Get method to retrieve Station by it's UUID
    def get_station_byuuid(self, uuid: int):
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_station = "SELECT uuid, nom, nbvelo, lon, lat, arrondissement FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sql_get_station, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_uuid = res['uuid']
            station_name = res['nom']
            station_nbvelo = res['nbvelo']
            station_lon = res['lon']
            station_lat = res['lat']
            station_loc = Location(station_lon, station_lat)
            station = Station(station_uuid, station_name, station_loc, station_nbvelo)
            return station
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station by it's UUID
    def get_station_name_byuuid(self, uuid: int):
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_station = "SELECT nom FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sql_get_station, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_name = res['nom']
            return station_name
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station's arrondissement by it's UUID
    def get_station_arr_byuuid(self, uuid: int):
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_station_arr = "SELECT arrondissement FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sql_get_station_arr, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_arr = res['arrondissement']
            return station_arr
        return f"unable to find a station arrondissement with UUID = {uuid}"    
    
    # Get method to retrieve Station's location by it's UUID
    def get_station_loc_byuuid(self, uuid: int):
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_station_loc = "SELECT lon, lat FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sql_get_station_loc, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_loc = res['lon'], res['lat']
            return station_loc
        return f"unable to find a station arrondissement with UUID = {uuid}" 
    
    # Get method to retrieve Station's bikes available by its UUID
    def get_station_numbikes_byuuid(self, uuid: int):
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_get_station_num_bikes = "SELECT nbvelo FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sql_get_station_num_bikes, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_numbikes = res['nbvelo']
            return station_numbikes
        return f"unable to find a station's bikes number with UUID = {uuid}" 
    
    
    def update_station(self, station: Station):
        
        updated = False
        
        with Database.get_connection as connection:
            cursor = connection.cursor()
            sql_update_station = """UPDATE Station SET nom = %(nom)s, 
                                                    arrondissement = %(arrondissement)s,
                                                    nbvelo = %(nbvelo)s,
                                                    lon = %(lon)s,
                                                    lat = %(lat)s,
                                                    WHERE uuid = %(uuid)s"""
            cursor.execute(sql_update_station, {"nom": station.get_station_name,
                                                "arrondissement": station.get_station_arr,
                                                "nbvelo": station.get_station_num_bikes,
                                                "lon": station.get_station_lon,
                                                "lat": station.get_station_lat,
                                                "uuid": station.get_station_id})
            res = cursor.fetchone()
        if res:
            return not(updated)
        return updated