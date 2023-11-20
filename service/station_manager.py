from schema.station import Station
from schema.location import Location
from schema.date import Date
from schema.record import Record
from database.dao_station import DAOStation
from database.dao_date import DAODate
from database.dao_record import DAORecord
from vincenty import vincenty
from datetime import datetime
import requests
import time


class StationManager():

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_stations(self):
        # Initialize an HTTP client
        with requests.Session() as session:
            try:
                # Send a GET request to the OpenDataSoft API
                response = session.get(self.base_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Return the JSON response from the API
                    return response.json()
                else:
                    # Handle error cases
                    return {"error": f"Request failed with status code {response.status_code}"}
            except Exception as e:
                return {"error": str(e)}

    def get_available_station(data):

        data_station = data
        velib_data = []

        for records in data_station:
            station_id = records["stationcode"]
            station_name = records["name"]
            lat = float((records['coordonnees_geo']['lat']))
            lon = float((records['coordonnees_geo']['lon']))
            numbikes = int((records['numbikesavailable']))
            locdict = {
                "lat": lat,
                "lon": lon
            }
            loc = Location(**locdict)
            new_record = {
                'station': {
                    'station_name': station_name,
                    'station_uuid': station_id,
                    'loc': loc,
                    'numbikes': numbikes},
            }
            if numbikes > 0:
                velib_data.append(new_record)

        return {'velibs': velib_data}

    def get_nearest_station(data, loc) -> Station:

        data_station = data
        distance = []

        for station in data_station["velibs"]:
            station_loc = station["station"]["loc"]
            dist = vincenty(loc, station_loc.get_location)
            distance.append((dist, station["station"]))

        nearest_station = min(distance)[1]
        return Station(**nearest_station)

    def fill_tables(self, data):

        data_station = data

        for records in data_station:
            station_uuid = records['stationcode']
            station_name = records['name']
            lat = float((records['coordonnees_geo']['lat']))
            lon = float((records['coordonnees_geo']['lon']))
            nbvelo = records['numbikesavailable']
            station_loc = Location(lon=lon, lat=lat)

            new_station = Station(station_uuid=station_uuid, station_name=station_name, loc=station_loc, numbikes=nbvelo)

            DAOStation.add_new_station(station=new_station)

        new_date = Date().get_date
        DAODate.add_new_date(date_time=new_date)

    def refresh_station_every_minute(self):

        while True:

            current_timestamp = datetime.now().replace(second=0)
            formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            data_station = self.get_stations()

            DAODate.add_new_date(formatted_timestamp)

            for records in data_station:
                station_id = records['stationcode']
                station_name = records['name']
                lat = float((records['coordonnees_geo']['lat']))
                lon = float((records['coordonnees_geo']['lon']))
                station_loc = Location(lat=lat, lon=lon)
                nbvelo = records['numbikesavailable']

                update_station = Station(station_uuid=station_id, station_name=station_name, loc=station_loc, numbikes=nbvelo)

                try:
                    previous_num_bikes = DAOStation.get_station_numbikes_byuuid(uuid=station_id)
                    DAOStation.update_station(station=update_station)
                    actual_num_bikes = DAOStation.get_station_numbikes_byuuid(uuid=station_id)
                    if abs(actual_num_bikes - previous_num_bikes) > 0:
                        variation = abs(actual_num_bikes - previous_num_bikes)
                        date_uuid = DAODate.get_uuid_bydate(date=Date().get_date)
                        new_record = Record(station_uuid=station_id, date_uuid=int(date_uuid), variation=variation)
                        DAORecord.add_new_record(record=new_record)
                finally:
                    pass
            time.sleep(60)
