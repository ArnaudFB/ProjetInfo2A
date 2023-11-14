# Import necessary modules
import requests
from fastapi import FastAPI, Request, Query
import uvicorn
import json
import httpx
from schema.location import Location
from schema.station import Station
from service.station_manager import StationManager
from schema.location import Location

from service.station_manager import StationManager

from database.dao_record import DAORecord
from database.init_db import Database
from service.station_manager import StationManager
from datetime import datetime



# Creating API
app = FastAPI()

@app.get("/fonctionnalite-1/", response_model=str)
async def getNearestStation(user_location: str = Query(Location(lat=48.8563199,lon=2.31345367))):
    
    user_location = tuple(map(float, user_location.split(',')) if ',' in user_location else (48.8563199, 2.31345367))

    # Base URL for the app
    BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"
    
    station = await StationManager(BASE_URL).get_stations()
    
    station = StationManager.get_available_station(station)
    
    station = StationManager.get_nearest_station(station, user_location)
    
    return f"La station la plus proche est la station {station}"
    


@app.get("/fonctionnalite-2/")    
async def getLeastFreqStat(date_debut : datetime, date_fin : datetime):

    station_moins_frequente=DAORecord.get_min_frequentation_station(date_debut,date_fin)
     
    
    return f"La station la moins fréquentée entre {date_debut} et {date_fin} : {station_moins_frequente}"



@app.get("/fonctionnalite-3/")    
async def getFreqArr(date_debut : datetime, date_fin : datetime):
        
    arrondissement_plus_frequente = DAORecord.get_max_frequentation_arrondissement(date_debut,date_fin)
    
    return f"L'arrandissement le plus fréquentée entre {date_debut} et {date_fin} : {arrondissement_plus_frequente}"
    




@app.get("/fonctionnalite-2/")    
async def getLeastFreqStat(date_debut : datetime, date_fin : datetime):

    station_moins_frequente=DAORecord.get_min_frequentation_station(date_debut,date_fin)
     
    
    return f"La station la moins fréquentée entre {date_debut} et {date_fin} : {station_moins_frequente}"



@app.get("/fonctionnalite-3/")    
async def getFreqArr(date_debut : datetime, date_fin : datetime):
        
    arrondissement_plus_frequente = DAORecord.get_max_frequentation_arrondissement(date_debut,date_fin)
    
    return f"L'arrandissement le plus fréquentée entre {date_debut} et {date_fin} : {arrondissement_plus_frequente}"
    



if __name__ == "__main__":
    print("Starting server")
    uvicorn.run(app, host = "127.0.0.1", port = 8000)