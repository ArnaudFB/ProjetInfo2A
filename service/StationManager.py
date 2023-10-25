from data.Station import Station
from data.Location import Location
from database.DAOStation import DAOStation
from vincenty import vincenty
import httpx

class StationManager():
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def getStations(self):
        # Initialize an HTTP client
        async with httpx.AsyncClient() as client:
            try:
                # Send a GET request to the OpenDataSoft API
                response = await client.get(self.base_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Return the JSON response from the API 
                    return response.json()
                
                else:
                    # Handle error cases
                    return {"error": f"Request failed with status code {response.status_code}"}
            except Exception as e:
                return {"error": str(e)}  
    
    def getAvailableStation(data):
        
        data_station = data
        velib_data = []
                
        for records in data_station:
            station_id=records['stationcode']
            station_name=records['name']
            lat=float((records['coordonnees_geo']['lat']))
            lon=float((records['coordonnees_geo']['lon']))
            numbikes=int((records['numbikesavailable']))
            new_record={
                'station': {
                    'name':station_name,
                    'uuid':station_id,
                    'latitude':lat,
                    'longitude':lon,
                    'numbikesavailable':numbikes},
                }
            if numbikes > 0:
                velib_data.append({**new_record})
                    
        return {'velibs':velib_data}
        
    
    def getNearestStation(data, loc) -> int:
        
        data_station = data
        distance = []
        
        for station in data_station["velibs"]:
            
            dist = vincenty(loc, (station["station"]["longitude"],station["station"]["latitude"]))
            distance.append((dist, station["station"]["uuid"]))
        
        nearest_station = min(distance)[1]
        return nearest_station
        
        