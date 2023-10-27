from schema.record import Record
from schema.location import Location
class Station:
    
    def __init__(self, station_id: int,station_name: str, loc: Location, numbikes: int):
        self._stationId = station_id
        self._stationName = station_name
        self.__loc = loc
        self.__numbikes = numbikes
        station_arr = station_id[:-3]
        if station_arr > 20:
            self._stationArr = 0
        self._stationArr = station_arr
                    
    @property
    def getStationID(self) -> int:
        return self._stationId
            
    @property
    def getStationName(self) -> str:
        return self._stationName
    
    @property
    def getStationNumBikes(self) -> int:
        return self.__numbikes
    
    @property
    def getStationCoordinates(self) -> tuple[float]:
        return self.__loc.getLocation
    
    @property
    def getStationLon(self) -> float:
        return self.__loc.getLongitude
    
    @property
    def getStationLat(self) -> float:
        return self.__loc.getLatitude
    
    @property
    def getStationArr(self) -> int:
        return self._stationArr
    