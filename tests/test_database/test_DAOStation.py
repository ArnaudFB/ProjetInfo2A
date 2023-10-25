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
        dao_station.execute = MagicMock(return_value={'uuid': '123', 'nom': 'Station A', 'lon': 10.0, 'lat': 20.0})

        #When
        result = dao_station.getStationByUUID('123')

        # then
        self.assertIsInstance(result, Station)
        self.assertEqual(result.getStationID(), '123')
        self.assertEqual(result.getStationName(), 'Station A')
        self.assertEqual(result.getStationLocation().getLongitude(), 10.0)
        self.assertEqual(result.getStationLocation().getLatitude(), 20.0)

    def test_nonexistant_getStationbyUUID(self): 
        dao_station = DAOStation()
        dao_station.execute = MagicMock(return_value=None)  

        with self.assertRaises(Exception) as context:
            result = dao_station.getStationByUUID('nonexistent_uuid')

        self.assertEqual(str(context.exception), "unable to find a station name with UUID = nonexistent_uuid")

if __name__ == '__main__':
    unittest.main()
