import unittest
from unittest.mock import MagicMock
from database import dao_record
from schema import record
from datetime import datetime 

class TestDAORecord(unittest.TestCase):

    def setUp(self):
        self.record = record.Record(123, 5, 7)
        self.self.dao_record = dao_record()
        self.existing_station_uuid = 16107
        self.non_existing_station_uuid = 99999
        self.date_start = datetime.datetime(2023, 10, 28)
        self.date_end = datetime.datetime(2023, 10, 31)
        self.existing_arrondissement = 16

    def test_add_new_record(self):
 
        self.dao_record.execute = MagicMock(return_value={'station_uuid': 123})

       
        created = self.dao_record.addNewStation(self.record)
      
        self.assertTrue(created)

   
    def test_add_new_record_error(self):
    

        self.dao_record.execute = MagicMock(return_value="Database connection error")

        
        with self.assertRaises(Exception) as context:
            created = self.dao_record.addNewStation(self.station)

        self.assertEqual(str(context.exception), "Database connection error")


    def test_get_var_bystation_date_existing_station(self):
        
        records = self.dao_record.getRecordByStationDate(self.existing_station_uuid, self.date_start, self.date_end)

        
        self.assertIsInstance(records, list)
        self.assertTrue(len(records) > 0)

    def test_get_var_bystation_date_non_existing_station(self):
        
        result = self.dao_record.getVarByStationDate(self.non_existing_station_uuid, self.date_start, self.date_end)

        
        self.assertEqual(result, f"unable to find a record for station {self.non_existing_station_uuid} between {self.date_start} and {self.date_end}")

    def test_get_var_groupstation_bydate_existing(self):
        # Action
        records = self.dao_record.getVarByDate(self.date_start, self.date_end)

        # Assertion
        self.assertIsInstance(records, list)
        self.assertTrue(len(records) > 0)

    def test_get_var_groupstation_bydate_invalid_dates(self):
        # Test avec des dates invalides (hors de la plage)
        date_start = datetime.datetime(2022, 12, 30)
        date_end = datetime.datetime(2023, 12, 31)

        result = self.dao_record.getVarByDate(date_start, date_end)
        self.assertEqual(result, f"unable to find a record between {date_start} and {date_end}")

    def test_get_var_groupstation_bydate_database_error(self):
        # Test pour simuler une erreur de base de données
        date_start = datetime.datetime(2023, 1, 1)
        date_end = datetime.datetime(2023, 1, 5)

        self.dao_record.getConnection = MagicMock(side_effect=Exception("Database connection error"))

        result = self.dao_record.getVarByDate(date_start, date_end)
        self.assertEqual(result, "Database connection error")


    def test_get_var_byarr_date_existing_records(self):

        dao_record = DAORecord()  

        result = dao_record.getVarByArrDate(self.existing_arrondissement, self.date_start, self.date_end)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_var_byarr_date_no_records(self):
        dao_record = DAORecord()
        arrondissement = 30 
        
        result = dao_record.getVarByArrDate(arrondissement, self.date_start, self.date_end)
        self.assertEqual(result, f"unable to find a record between {self.date_start} and {self.date_end} in arrondissement {arrondissement}")


    def test_get_var_byarr_date_invalid_dates(self):
        dao_record = DAORecord()

        date_start = datetime.datetime(2023, 1, 5)  # Date de fin antérieure à la date de début
        date_end = datetime.datetime(2023, 1, 1)

        result = dao_record.getVarByArrDate(self.existing_arrondissement, date_start, date_end)
        self.assertEqual(result, f"unable to find a record between {date_start} and {date_end} in arrondissement {self.existing_arrondissement}")

    def test_get_var_grouparr_bydate_existing_records(self):
        
        dao_record = DAORecord()

        result = dao_record.getVarByArrDate(self.existing_arrondissement, self.date_start, self.date_end)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_var_grouparr_bydate_no_records(self):

        dao_record = DAORecord()
        arrondissement = 999  


        result = dao_record.getVarByArrDate(arrondissement, self.date_start, self.date_end)
        self.assertEqual(result, f"unable to find a record between {self.date_start} and {self.date_end} in arrondissement {arrondissement}")

    def test_get_var_grouparr_bydate_invalid_dates(self):
        # Test avec des dates invalides
        dao_record = DAORecord()
        date_start = datetime.datetime(2023, 1, 5)  
        date_end = datetime.datetime(2023, 1, 1)

        result = dao_record.getVarByArrDate(self.arrondissement, date_start, date_end)
        self.assertEqual(result, f"unable to find a record between {date_start} and {date_end} in arrondissement {self.arrondissement}")

if __name__ == '__main__':
    unittest.main()