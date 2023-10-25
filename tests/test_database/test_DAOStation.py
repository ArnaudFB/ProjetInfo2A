import unittest
from unittest.mock import MagicMock
from database import DAOStation
from data import Station, Location

class TestDAOStation(unittest.TestCase):

    def setUp(self):
        # Initialisation des objets nécessaires aux tests
        self.station = Station.Station(123, 'Station A', Location(10.0, 20.0))

    def test_addNewStation(self):
 
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value={'stationid': 123})

       
        created = dao_station.addNewStation(self.station)
      
        self.assertTrue(created)

   
    def test_addNewStation_error(self):
    
        dao_station = DAOStation()
        dao_station.getConnection = MagicMock(side_effect=Exception("Database connection error"))

        
        with self.assertRaises(Exception) as context:
            created = dao_station.addNewStation(self.station)

        self.assertEqual(str(context.exception), "Database connection error")


    def test_getStationByUUID(self):
        #GIVEN
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value={'uuid': 12563, 'nom': 'Station A', 'lon': 10.0, 'lat': 20.0})

        #When
        result = dao_station.getStationByUUID(12563)

        # then
        self.assertIsInstance(result, Station)
        self.assertEqual(result.getStationID(), 12563)
        self.assertEqual(result.getStationName(), 'Station A')
        self.assertEqual(result.getStationLocation().getLongitude(), 10.0)
        self.assertEqual(result.getStationLocation().getLatitude(), 20.0)

    def test_nonexistant_getStationbyUUID(self): 
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.getStationByUUID('nonexistent_uuid')

        self.assertEqual(str(context.exception), "unable to find a station name with UUID = nonexistent_uuid")


    def test_getStationArrByUUID_existing_station(self):
        # Test avec une station existante
        dao_station = DAOStation()
        uuid=16107
        result =dao_station.getStationArrByUUID(uuid)
        self.assertEqual(result, 16)

    def test_getStationArrByUUID_non_existing_station(self):
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.getStationByUUID('nonexistent_uuid')

        self.assertEqual(result, f"unable to find a station arrondissement with UUID = nonexistent_uuid ")

    def test_getStationLocByUUID_existing_station(self):
        dao_station = DAOStation()
        uuid = 16107

        result = your_instance.getStationLocByUUID(uuid)
        self.assertEqual(result, (48.865983, 2.275725))  

    def test_getStationLocByUUID_non_existing_station(self):
        # Test avec une station inexistante
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.getStationByUUID('nonexistent_uuid')
    
        self.assertEqual(result, f"unable to find a station location with UUID = 'nonexistent_uuid'")


if __name__ == '__main__':
    unittest.main()
