# Import necessary modules
import requests
from fastapi import FastAPI, Request
import uvicorn
import json
import httpx
from data.Location import Location


# Creating API
app = FastAPI()
         
@app.get("/fonctionnalite-1")    
async def getNearestStation(loc : Location):
    
    station = getStations().getAvailableStations().getNearestStation(loc)
    
    return station
    
            

if __name__ == "__main__":
    print("Starting server")
    uvicorn.run(app, host = "127.0.0.1", port = 8000)