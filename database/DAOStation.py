from database.init_db import Database
from utils.Singleton import Singleton
from data.Station import Station
from data.Location import Location
import sqlite3


class DAOStation(metaclass=Singleton):
    
    # Create method to get all Station in the database
    def getAllStation(self, station: Station) -> dict[Station]:
        
        with Database.getConnection as connection: # gets a database connection 
            cursor = connection.cursor() # creates a cursor object to execute SQL queries 
            sqlGetAllStation = """SELECT * FROM Station;""" #SQL query to select all stations 
            cursor.execute(sqlGetAllStation)
            res = cursor.fetchall() # retrieves all rows in the query result as a dictionary 
        
        return
    
    # Create method to create a new Station in the database
    def addNewStation(self, station: Station) -> bool:
        
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
    def getStationByUUID(self, uuid: int):
        
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
            station_loc = Location(station_lon, station_lat) # creates a Location object with the retrieved coordinates 
            station = Station(station_uuid, station_name, station_loc, station_nbvelo) # creates a Station object with the retrieved informations 
            return station
        return f"unable to find a station name with UUID = {uuid}"
    
    # Get method to retrieve Station by it's UUID
    def getStationNameByUUID(self, uuid: int):
        
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
    def getStationArrByUUID(self, uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStationArr = "SELECT arrondissement FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStationArr, {"uuid": uuid}) # executes the request using the supplied UUID
            res = cursor.fetchone()
        if res:
            station_arr = res['arrondissement']
            return station_arr
        return f"unable to find a station arrondissement with UUID = {uuid}"    
    
    # Get method to retrieve Station's location by it's UUID
    def getStationLocByUUID(self, uuid: int):
        
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
    def getStationNumBikesByUUID(self, uuid: int):
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlGetStationNumBikes = "SELECT nbvelo FROM Station WHERE uuid = %(uuid)s"
            cursor.execute(sqlGetStationNumBikes, {"uuid": uuid})
            res = cursor.fetchone()
        if res:
            station_numbikes = res['nbvelo']
            return station_numbikes
        return f"unable to find a station's bikes number with UUID = {uuid}" 
    
    
    def updateStation(self, station: Station):
        
        updated = False
        
        with Database.getConnection as connection:
            cursor = connection.cursor()
            sqlUpdateStation = """UPDATE Station SET nom = %(nom)s, 
                                                    arrondissement = %(arrondissement)s,
                                                    nbvelo = %(nbvelo)s,
                                                    lon = %(lon)s,
                                                    lat = %(lat)s,
                                                    WHERE uuid = %(uuid)s"""
            cursor.execute(sqlUpdateStation, {"nom": station.getStationName,
                                                "arrondissement": station.getStationArr,
                                                "nbvelo": station.getStationNumBikes,
                                                "lon": station.getStationLon,
                                                "lat": station.getStationLat,
                                                "uuid": station.getStationID})
            res = cursor.fetchone()
        if res:
            return not(updated)
        return updated