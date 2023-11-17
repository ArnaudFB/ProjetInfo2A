# Import necessary modules
from fastapi import FastAPI, Query
import uvicorn

from schema.location import Location
from schema.station import Station

from database.dao_record import DAORecord
from database.init_db import Database

from service.station_manager import StationManager

from datetime import datetime



# Creating API
app = FastAPI()
# Base URL for the app
BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"

@app.get("/fonctionnalite-1/", response_model=Station)
async def get_nearest_station(user_location: str = Query(Location(**{'lon':48.8563199, 'lat':2.31345367}))):
    
    user_location = tuple(map(float, user_location.split(',')) if ',' in user_location else (48.8563199, 2.31345367))

    station = await StationManager(BASE_URL).get_stations()
    
    station = StationManager.get_available_station(station)
    
    station = StationManager.get_nearest_station(station, user_location)
    
    return station

@app.get("/fonctionnalite-2/")    
async def get_least_freq_stat(date_debut : datetime, date_fin : datetime):

    station_moins_frequente=DAORecord.get_min_frequentation_station(date_debut,date_fin)
    
    return f"La station la moins fréquentée entre {date_debut} et {date_fin} : {station_moins_frequente}"

@app.get("/fonctionnalite-3/")    
async def get_freq_arr(date_debut : datetime, date_fin : datetime):
        
    arrondissement_plus_frequente = DAORecord.get_max_frequentation_arrondissement(date_debut,date_fin)
    
    return f"L'arrandissement le plus fréquentée entre {date_debut} et {date_fin} : {arrondissement_plus_frequente}"
    
if __name__ == "__main__":
    print("Starting server")
    uvicorn.run(app, host = "127.0.0.1", port = 8000)

'''
    data = await StationManager(BASE_URL).get_stations()
    StationManager(BASE_URL).fill_tables(data)'''