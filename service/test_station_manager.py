import unittest
from database.dao_record import DAORecord  
from database.dao_station import DAOStation
from service.station_manager import StationManager
from schema.location import Location
class TestStationManager(unittest.TestCase):

    def test_get_available_station(self):
        # Simulez les données de l'API
        data = [
            {
                "stationcode": "12345",
                "name": "Station 1",
                "coordonnees_geo": {
                    "lat": 48.856614,
                    "lon": 2.352221
                },
                "numbikesavailable": 5
            },
            {
                "stationcode": "54321",
                "name": "Station 2",
                "coordonnees_geo": {
                    "lat": 48.859517,
                    "lon": 2.349973
                },
                "numbikesavailable": 0
            }
        ]

        # Appelez la fonction et obtenez les stations disponibles
        available_stations = StationManager.get_available_station(data)

        # Vérifiez que le résultat est correct
        self.assertEqual(len(available_stations["velibs"]), 1)
        self.assertEqual(available_stations["velibs"][0]["station"]["station_name"], "Station 1")
        self.assertEqual(available_stations["velibs"][0]["station"]["numbikes"], 5)

    def test_get_nearest_station(self):
        # Simulez les données de l'API et la localisation de l'utilisateur
        data = {
            "velibs": [
                {
                    "station": {
                        "station_name": "Station 1",
                        "station_uuid": "12345",
                        "loc": Location(lat=48.856614, lon=2.352221),
                        "numbikes": 5
                    }
                },
                {
                    "station": {
                        "station_name": "Station 2",
                        "station_uuid": "54321",
                        "loc": Location(lat=48.859517, lon=2.349973),
                        "numbikes": 0
                    }
                }
            ]
        }

        user_loc = Location(lat=48.856614, lon=2.352221)

        # Appelez la fonction et obtenez la station la plus proche
        nearest_station = StationManager.get_nearest_station(data, user_loc)

        # Vérifiez que le résultat est correct
        self.assertEqual(nearest_station["station_name"], "Station 1")

    def test_fill_tables(self):
        # Simulez les données de l'API
        data = [
            {
                "stationcode": "12345",
                "name": "Station 1",
                "coordonnees_geo": {
                    "lat": 48.856614,
                    "lon": 2.352221
                },
                "numbikesavailable": 5
            },
            {
                "stationcode": "54321",
                "name": "Station 2",
                "coordonnees_geo": {
                    "lat": 48.859517,
                    "lon": 2.349973
                },
                "numbikesavailable": 0
            }
        ]

        # Appelez la fonction pour remplir les tables
        StationManager.fill_tables(data)

        # Vérifiez que les stations ont été ajoutées à la table Station
        stations = DAOStation.get_all_stations()
        self.assertEqual(len(stations), 2)

        # Vérifiez que les enregistrements ont été ajoutés à la table Record
        records = DAORecord.get_all_records()
        self.assertEqual(len(records), 0)
if __name__ == '__main__':
    unittest.main()
    