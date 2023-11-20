# Import necessary modules
from fastapi import FastAPI, Query
import uvicorn
import requests

from schema.location import Location
from schema.station import Station

from service.station_manager import StationManager
from service.record_manager import RecordManager

from datetime import datetime



# Creating API
app = FastAPI()
# Base URL for the app
BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"
ETALAB_GEO_API = "https://api-adresse.data.gouv.fr/search/"
class ApiVelib():
    @app.get("/fonctionnalite-1/", response_model=Station)
    def get_nearest_station(user_location: str = Query(Location(**{'lon':48.8563199, 'lat':2.31345367}))):

        user_location = tuple(map(float, user_location.split(',')) if ',' in user_location else (48.8563199, 2.31345367))

        station =  StationManager(BASE_URL).get_stations()

        station = StationManager.get_available_station(station)

        station = StationManager.get_nearest_station(station, user_location)

        return station
    @app.get("/fonctionnalite-2/", response_model=Station)
    def get_least_freq_stat(date_debut : datetime, date_fin : datetime, period = Query("d") ):

        station_moins_frequente = RecordManager.get_min_frequentation_station(date_debut,date_fin,period)

        return station_moins_frequente

    @app.get("/fonctionnalite-3/", response_model=int)
    def getFreqArr(date_debut : datetime, date_fin : datetime, period = Query("d") ):

        arrondissement_plus_frequente = RecordManager.get_max_frequentation_arrondissement(date_debut,date_fin, period)

        return arrondissement_plus_frequente

    @app.get("/fonctionnalite-3/")
    def get_freq_arr(date_debut : datetime, date_fin : datetime):

        arrondissement_plus_frequente = RecordManager.get_max_frequentation_arrondissement(date_debut,date_fin)

        return f"L'arrandissement le plus fréquentée entre {date_debut} et {date_fin} : {arrondissement_plus_frequente}"

    def run_api():
        print("Starting server")
        uvicorn.run(app, host="127.0.0.1", port=8000)

    @app.get("/get_geographic_data/")
    async def get_geographic_data(address: str ):
        params = {'q': address, 'limit': 1}
        response = requests.get(ETALAB_GEO_API, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get('features'):
                geographic_data = data['features'][0]['geometry']['coordinates']
                user_location = {'lon': geographic_data[0], 'lat': geographic_data[1]}
                return user_location
            else:
                return {"message": "Aucune donnée géographique trouvée pour cette adresse."}
        else:
            return {"message": "Erreur lors de la récupération des données géographiques."}

    def get_nearest_station_address(self, user_address: str):
        geographic_data = self.get_geographic_data(user_address)

        station = StationManager(BASE_URL).get_stations()
        station = StationManager.get_available_station(station)
        station = StationManager.get_nearest_station(station, geographic_data)
        return station



