import unittest
from datetime import datetime
from database.dao_record import DAORecord  
from service.record_manager import RecordManager
class TestRecordManager(unittest.TestCase):
    def test_get_min_frequentation_station(self):
        # Simulez la méthode DAORecord.get_var_groupstation_bydate
        DAORecord.get_var_groupstation_bydate = lambda start, end: [(1, 10), (2, 5), (3, 15)]

        # Testez avec des dates d'exemple
        result = RecordManager.get_min_frequentation_station(datetime(2023, 1, 1), datetime(2023, 1, 10))
        self.assertEqual(result, 2)  # Remplacez par le résultat attendu

    def test_get_max_frequentation_arrondissement(self):
        # Simulez la méthode DAORecord.get_var_grouparr_bydate
        DAORecord.get_var_grouparr_bydate = lambda start, end: [(1, 30), (2, 20), (3, 10)]

        # Testez avec des dates d'exemple
        result = RecordManager.get_max_frequentation_arrondissement(datetime(2023, 1, 1), datetime(2023, 1, 10))
        self.assertEqual(result, 1)  # Remplacez par le résultat attendu

if __name__ == '__main__':
    unittest.main()

