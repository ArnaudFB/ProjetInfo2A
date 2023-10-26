from data.Date import Date
from datetime import datetime

class Record:

    def __init__(self, station_uuid: int, date_uuid: int, variation: int):
        if variation< 0:
            raise ValueError("Variation must be positive !")
        if not(isinstance(station_uuid,int)) or not(isinstance(station_uuid,int)) :
            raise TypeError("uuid must be integers")

        else:
            self.station_uuid = station_uuid
            self.dat_uuid = date_uuid
            self.variation = variation
  
            
    @property
    def getStationUuid(self) -> int:
        return self.station_uuid

    @property
    def getDateUuid(self) -> int:
        return self.date_uuid

    @property
    def getVariation(self) -> int:
        return self.variation

    
    