from api.api_handler import ApiVelib
from service.station_manager import StationManager
import threading

api_thread = threading.Thread(target=ApiVelib.run_api)
api_thread.daemon = True
api_thread.start()

BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"

while True:
    StationManager(BASE_URL).refresh_station_every_minute()

