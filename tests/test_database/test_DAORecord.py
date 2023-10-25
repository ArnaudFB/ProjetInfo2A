import unittest
from unittest.mock import MagicMock
from database import DAORecord
from data import Record


class TestDAORecord(unittest.TestCase):

    def setUp(self):
        self.record = Record.Record(123, 5, 7)
        self.dao_record = DAORecord()
        self.existing_station_uuid = 123
        self.non_existing_station_uuid = 456
        self.date_start = datetime.datetime(2023, 1, 1)
        self.date_end = datetime.datetime(2023, 1, 5)

    def test_addNewRecord(self):
 
        dao_record = DAORecord()
        dao_record.execute = MagicMock(return_value={'station_uuid': 123})

       
        created = dao_record.addNewStation(self.record)
      
        self.assertTrue(created)

   
    def test_addNewRecord_error(self):
    
        dao_record = DAORecord()
        dao_record.execute = MagicMock(return_value="Database connection error")

        
        with self.assertRaises(Exception) as context:
            created = dao_record.addNewStation(self.station)

        self.assertEqual(str(context.exception), "Database connection error")


    def test_getRecordByStationDate_existing_station(self):
        # Action
        records = self.dao_record.getRecordByStationDate(self.existing_station_uuid, self.date_start, self.date_end)

        # Assertion
        self.assertIsInstance(records, list)
        self.assertTrue(len(records) > 0)

    def test_getRecordByStationDate_non_existing_station(self):
        # Action
        result = self.dao_record.getRecordByStationDate(self.non_existing_station_uuid, self.date_start, self.date_end)

        # Assertion
        self.assertEqual(result, f"unable to find a record for station {self.non_existing_station_uuid} between {self.date_start} and {self.date_end}")

    
if __name__ == '__main__':
    unittest.main()