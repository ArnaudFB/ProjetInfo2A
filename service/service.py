import time
from datetime import datetime

import requests
from vincenty import vincenty

from database.dao_date import DAODate
from database.dao_record import DAORecord
from database.dao_station import DAOStation
from schema.date import Date
from schema.location import Location
from schema.record import Record
from schema.station import Station


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

    def get_geographic_data(address: str):
        ETALAB_GEO_API = "https://api-adresse.data.gouv.fr/search/"
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

    def get_min_frequentation_station(date_start: datetime, date_end: datetime, cutting: str) -> int:
        number_d = (date_end - date_start).days
        number_w = number_d // 7
        number_m = number_d // 30.44  # durée moyenne d'un m
        number_h = (number_d * 24)

        variation = DAORecord.get_var_groupstation_bydate(date_start, date_end)

        less_frequented_station_uuid = min(variation)[0]
        '''key=lambda t: t[1] / globals()['number_{}'.format(cutting)]'''
        station = DAOStation.get_station_byuuid(less_frequented_station_uuid)

        return station

    def get_max_frequentation_arrondissement(date_start: datetime, date_end: datetime, cutting: str) -> int:
        number_d = (date_end - date_start).days
        number_w = number_d // 7
        number_m = number_d // 30.44  # durée moyenne d'un m
        number_h = (number_d * 24)
        variation = DAORecord.get_var_grouparr_bydate(date_start, date_end)
        more_frequented_arr = max(variation)[0]
        '''key=lambda t: t[1] / globals()['number_{}'.format(cutting)]'''
        return more_frequented_arr

    def fill_tables(self, data):

        data_station = data

        for records in data_station:
            station_uuid = records['stationcode']
            station_name = records['name']
            lat = float((records['coordonnees_geo']['lat']))
            lon = float((records['coordonnees_geo']['lon']))
            nbvelo = records['numbikesavailable']
            station_loc = Location(lon=lon, lat=lat)

            new_station = Station(station_uuid=station_uuid, station_name=station_name, loc=station_loc,
                                  numbikes=nbvelo)

            DAOStation.add_new(station=new_station)

        new_date = Date().get_date
        DAODate.add_new(date_time=new_date)

    def refresh_station_every_minute(self):

        while True:

            current_timestamp = datetime.now().replace(second=0)
            formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')

            data_station = self.get_stations()

            DAODate.add_new(formatted_timestamp)

            for records in data_station:
                station_id = records['stationcode']
                station_name = records['name']
                lat = float((records['coordonnees_geo']['lat']))
                lon = float((records['coordonnees_geo']['lon']))
                station_loc = Location(lat=lat, lon=lon)
                nbvelo = records['numbikesavailable']

                update_station = Station(station_uuid=station_id, station_name=station_name, loc=station_loc,
                                         numbikes=nbvelo)

                try:
                    previous_num_bikes = DAOStation.get_station_numbikes_byuuid(uuid=station_id)
                    DAOStation.update_station(station=update_station)
                    actual_num_bikes = DAOStation.get_station_numbikes_byuuid(uuid=station_id)
                    if abs(actual_num_bikes - previous_num_bikes) > 0:
                        variation = abs(actual_num_bikes - previous_num_bikes)
                        date_uuid = DAODate.get_uuid_bydate(formatted_timestamp)
                        new_record = Record(station_uuid=station_id, date_uuid=int(date_uuid), variation=variation)
                        DAORecord.add_new(record=new_record)
                finally:
                    pass
            time.sleep(60)
