from database.init_db import Database
from utils.Singleton import Singleton
from data.Station import Station
from data.Location import Location
import sqlite3


class DAOStation(metaclass=Singleton):
    
    # Create method to get all Station in the database
    def getAllStation(self, station: Station) -> dict[Station]:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetAllStation = """SELECT * FROM Station;"""
            cursor.execute(sqlGetAllStation)
            res = cursor.fetchall()
        
        return
    
    # Create method to create a new Station in the database
    def addNewStation(self, station: Station) -> bool:
        
        created = False
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlAddStation = """INSERT INTO Station (uuid, arrondissement, nom, lon, lat)
                            VALUES (%(uuid)s,%(arrondissement)s %(name)s, %(lon)s, %(lat)s)"""
            cursor.execute(sqlAddStation, {"uuid": station.getStationID,
                                    "arrondissement": station.getStationArr,
                                    "name": station.getStationName,
                                    "lon": station.getStationLon,
                                    "lat": station.getStationLat})
            res = cursor.fetchone()
        if res:
            return not(created)
        return created
        
    # Get method to retrieve Station by it's UUID
    def getStationNameByUUID(uuid: int) -> str:
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStation = "SELECT nom FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStation, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_uuid = res['uuid']
            station_name = res['nom']
            station_lon = res['lon']
            station_lat = res['lat']
            station_loc = Location(station_lon, station_lat)
            station = Station(station_uuid, station_name, station_loc)
            return station
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station's arrondissement by it's UUID
    def getStationArrByUUID(uuid: int):
        
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
    def getStationLocByUUID(uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStationLoc = "SELECT lon, lat FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStationLoc, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_loc = res['lon'], res['lat']
            return station_loc
        return f"unable to find a station arrondissement with UUID = {uuid}" 