from schema.Station import Station
from schema.Location import Location
from schema.Date import Date
from schema.Record import Record
from database.DAOStation import DAOStation
from database.DAODate import DAODate
from database.DAORecord import DAORecord
from database.init_db import Database
from vincenty import vincenty
from datetime import datetime
import httpx
from database import DAORecord


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
            distance.append((dist, station["station"]["name"]))
        
        nearest_station = min(distance)[1]
        return nearest_station
    
        
    def fillTables(data):
        
        for records in data:
            station_id=records['stationcode']
            station_name=records['name']
            lat=float((records['coordonnees_geo']['lat']))
            lon=float((records['coordonnees_geo']['lon']))
            nbvelo=records['numbikesavailable']
            station_loc=Location(lon=lon, lat=lat)
            
            new_record_station={
                    'station_name':station_name,
                    'station_id':station_id,
                    'loc':station_loc,
                    'numbikes':nbvelo
                    },
            new_station = Station({**new_record_station})
            
            new_record_date={
                'date_minute': datetime.now().replace(second=0, microsecond=0)
            }
            new_date = Date({**new_record_date})
            
            DAOStation.addNewStation(station=new_station)
            DAODate.addNewDate(date=new_date)
    
    
    def refreshStationEveryMinute(data):
        
        data_station = data
        
        while True:
        
            for records in data_station:
                station_id=records['stationcode']
                station_name=records['name']
                lat=float((records['coordonnees_geo']['lat']))
                lon=float((records['coordonnees_geo']['lon']))
                station_loc=Location(lat=lat, lon=lon)
                nbvelo=records['numbikesavailable']
                new_record={
                        'station_name':station_name,
                        'station_id':station_id,
                        'loc':station_loc,
                        'numbikes':nbvelo
                        },
                update_station = Station({**new_record})
                    
                try:
                    previous_num_bikes=DAOStation.getStationNumBikesByUUID(uuid=station_id)
                    DAOStation.updateStation(station=update_station)
                    actual_num_bikes=DAOStation.getStationNumBikesByUUID(uuid=station_id)
                    DAODate.addNewDate(date=Date(datetime.now().replace(second=0, microsecond=0)))
                    if abs(actual_num_bikes-previous_num_bikes)>0:
                        variation=abs(actual_num_bikes-previous_num_bikes)
                        date_uuid=DAODate.getUUIDByDate(date=datetime.now().replace(second=0, microsecond=0))
                        new_record = Record(station_uuid=station_id, date_uuid=date_uuid, variation=variation)
                        DAORecord.addNewRecord(record=new_record)
                finally:
                    connection.close()
                
            time.sleep(60)
