# Import necessary modules
from typing import Optional

from fastapi import FastAPI, Query
import uvicorn

from schema.station import Station

from service.service import StationManager

from datetime import datetime

# Creating API
app = FastAPI()
# Base URL for the app
BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"

class ApiVelib():
    @app.get("/fonctionnalite-1/", response_model=Station)
    def get_nearest_station(user_adress: Optional[str] = Query(None), user_location: Optional[str] = Query(None)):

        if user_location:

            coordinates = tuple(map(float, user_location.split(','))) if ',' in user_location else None
            station = StationManager(BASE_URL).get_stations()
            station = StationManager.get_available_station(station)
            station = StationManager.get_nearest_station(station, coordinates)

            return station

        elif user_adress:

            geographic_data = StationManager.get_geographic_data(user_adress)
            geographic_data = tuple(geographic_data.values())
            station = StationManager(BASE_URL).get_stations()
            station = StationManager.get_available_station(station)
            station = StationManager.get_nearest_station(station, geographic_data)

            return station

        else:

            user_location = (48.8563199, 2.31345367)
            station =  StationManager(BASE_URL).get_stations()
            station = StationManager.get_available_station(station)
            station = StationManager.get_nearest_station(station, user_location)

            return station


    @app.get("/fonctionnalite-2/", response_model=Station)
    def get_least_freq_stat(date_debut : datetime = Query(datetime.min), date_fin : datetime = Query(datetime.now()), period = Query("d")):

        station_moins_frequente = StationManager.get_min_frequentation_station(date_debut, date_fin, period)

        return station_moins_frequente

    @app.get("/fonctionnalite-3/", response_model=int)
    def get_most_freq_arr(date_debut : datetime = Query(datetime.min), date_fin : datetime = Query(datetime.now()), period = Query("d") ):

        arrondissement_plus_frequente = StationManager.get_max_frequentation_arrondissement(date_debut,date_fin, period)

        return arrondissement_plus_frequente

    def run_api():
        print("Starting server")
        uvicorn.run(app, host="127.0.0.1", port=8000)

