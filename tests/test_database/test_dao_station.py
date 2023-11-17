import unittest
from unittest.mock import MagicMock
from database import DAOStation
from data import Station, Location

class TestDAOStation(unittest.TestCase):

    def setUp(self):
        # Initialisation des objets nécessaires aux tests
        self.station = station.Station(123, 'Station A', Location(10.0, 20.0))
        self.existing_uuid = 16107

    def test_add_new_station(self):
 
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value={'stationid': 123})

       
        created = dao_station.add_new_station(self.station)
      
        self.assertTrue(created)

   
    def test_add_new_station_error(self):
    
        dao_station = DAOStation()
        dao_station.getConnection = MagicMock(side_effect=Exception("Database connection error"))

        
        with self.assertRaises(Exception) as context:
            created = dao_station.add_new_station(self.station)

        self.assertEqual(str(context.exception), "Database connection error")


    def test_get_station_byuuid(self):
        #GIVEN
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value={'uuid': 12563, 'nom': 'Station A', 'lon': 10.0, 'lat': 20.0})

        #When
        result = dao_station.get_station_byuuid(12563)

        # then
        self.assertIsInstance(result, Station)
        self.assertEqual(result.get_station_id(), 12563)
        self.assertEqual(result.get_station_name(), 'Station A')
        self.assertEqual(result.getStationLocation().get_longitude(), 10.0)
        self.assertEqual(result.getStationLocation().get_latitude(), 20.0)

    def test_nonexistant_get_station_byuuid(self): 
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.get_station_byuuid('nonexistent_uuid')

        self.assertEqual(str(context.exception), "unable to find a station name with UUID = nonexistent_uuid")


    def test_get_station_arr_byuuid_existing_station(self):
        # Test avec une station existante
        dao_station = DAOStation()

        result =dao_station.get_station_arr_byuuid(self.existing_uuid)
        self.assertEqual(result, 16)

    def test_get_station_arr_byuuid_non_existing_station(self):
        dao_station = dao_station()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.get_station_arr_byuuid('nonexistent_uuid')

        self.assertEqual(result, f"unable to find a station arrondissement with UUID = nonexistent_uuid ")

    def test_get_station_loc_byuuid_existing_station(self):
        dao_station = DAOStation()
        result = dao_station.get_station_loc_byuuid(self.existing_uuid)
        self.assertEqual(result, (48.865983, 2.275725))  

    def test_get_station_loc_byuuid_non_existing_station(self):
        # Test avec une station inexistante
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.get_station_loc_byuuid('nonexistent_uuid')
    
        self.assertEqual(result, f"unable to find a station location with UUID = 'nonexistent_uuid'")

    def test_get_station_name_byuuid_existing_station(self):
        dao_station = DAOStation()
        result = dao_station.get_station_name_byuuid(self.existing_uuid)
        self.assertEqual(result, "Benjamin Godard - Victor Hugo")  

    def test_get_station_name_byuuid_non_existing_station(self):
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.get_station_name_byuuid('nonexistent_uuid')
    
        self.assertEqual(result,f"unable to find a station name with UUID = 'nonexistent_uuid'")
    


if __name__ == '__main__':
    unittest.main()
