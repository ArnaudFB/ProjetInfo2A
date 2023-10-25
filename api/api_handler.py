# Import necessary modules
import requests
from fastapi import FastAPI, Request, Query
import uvicorn
import json
import httpx
from data.Location import Location
from service.StationManager import StationManager


# Creating API
app = FastAPI()

@app.get("/fonctionnalite-1/")    
async def getNearestStation(user_location: str = Query((48.8563199, 2.31345367))):
    
    user_location = tuple(map(float, user_location.split(',')) if ',' in user_location else (48.8563199, 2.31345367))

    # Base URL for the app
    BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"
    
    station = await StationManager(BASE_URL).getStations()
    
    station = StationManager.getAvailableStation(station)
    
    station = StationManager.getNearestStation(station, user_location)
    
    return station
    
            

if __name__ == "__main__":
    print("Starting server")
    uvicorn.run(app, host = "127.0.0.1", port = 8000)