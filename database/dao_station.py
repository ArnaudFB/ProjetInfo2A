from database.init_db import Database
from utils.singleton import Singleton
from schema.station import Station
from schema.location import Location

import sqlite3


class DAOStation(metaclass=Singleton):
    
    # Create method to get all Station in the database
    def get_all_station(self, station: Station) -> dict[Station]:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetAllStation = """SELECT * FROM Station;"""
            cursor.execute(sqlGetAllStation)
            res = cursor.fetchall()
        
        return
    
    # Create method to create a new Station in the database
    def add_new_station(self, station: Station) -> bool:
        
        created = False
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlAddStation = """INSERT INTO Station (uuid, arrondissement, nom, nbvelo, lon, lat)
                            VALUES (%(uuid)s,%(arrondissement)s %(name)s, %(nbvelo)s, %(lon)s, %(lat)s)"""
            cursor.execute(sqlAddStation, {"uuid": station.getStationID,
                                    "arrondissement": station.getStationArr,
                                    "name": station.getStationName,
                                    "nbvelo": station.getStationNumBikes,
                                    "lon": station.getStationLon,
                                    "lat": station.getStationLat})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
        
    # Get method to retrieve Station by it's UUID
    def get_station_byuuid(self, uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStation = "SELECT uuid, nom, nbvelo, lon, lat, arrondissement FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStation, {"uuid": uuid})
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
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStation = "SELECT nom FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStation, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_name = res['nom']
            return station_name
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station's arrondissement by it's UUID
    def get_station_arr_byuuid(self, uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStationArr = "SELECT arrondissement FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStationArr, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_arr = res['arrondissement']
            return station_arr
        return f"unable to find a station arrondissement with UUID = {uuid}"    
    
    # Get method to retrieve Station's location by it's UUID
    def get_station_loc_byuuid(self, uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStationLoc = "SELECT lon, lat FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStationLoc, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_loc = res['lon'], res['lat']
            return station_loc
        return f"unable to find a station arrondissement with UUID = {uuid}" 
    
    # Get method to retrieve Station's bikes available by it's UUID
    def get_station_numbikes_byuuid(self, uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStationNumBikes = "SELECT nbvelo FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStationNumBikes, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_numbikes = res['nbvelo']
            return station_numbikes
        return f"unable to find a station's bikes number with UUID = {uuid}" 
    
    
    def update_station(self, station: Station):
        
        updated = False
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlUpdateStation = """UPDATE Station SET nom = %(nom)s, 
                                                    arrondissement = %(arrondissement)s,
                                                    nbvelo = %(nbvelo)s,
                                                    lon = %(lon)s,
                                                    lat = %(lat)s,
                                                    WHERE uuid = %(uuid)s"""
            cursor.execute(sqlGetStationLoc, {"nom": station.getStationName,
                                                "arrondissement": station.getStationArr,
                                                "nbvelo": station.getStationNumBikes,
                                                "lon": station.getStationLon,
                                                "lat": station.getStationLat,
                                                "uuid": station.getStationID})
            res = cursor.fetchone()
        if res:
            return not(updated)
        return updated