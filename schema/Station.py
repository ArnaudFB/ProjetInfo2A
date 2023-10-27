<<<<<<< HEAD
from schema.record import Record
from schema.location import Location
class Station:
=======
from pydantic import BaseModel, field_validator
from schema.Location import Location
class Station(BaseModel):
    
    station_uuid: int
    station_name: str
    loc: Location
    numbikes: int
    station_arr: int
    
    @field_validator("station_uuid")
    def station_uuid_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("station_uuid should be an integer")
        if v<0:
            raise ValueError("station_uuid cannot be negative")
        
    @field_validator("station_name")
    def station_uuid_not_valid(cls, v):
        if not isinstance(v, str):
            raise TypeError("station_uuid should be a string")

    @field_validator("loc")
    def station_uuid_not_valid(cls, v):
        if not isinstance(v, Location):
            raise TypeError("station_uuid should be a location")
        
    @field_validator("numbikes")
    def station_uuid_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("numbikes should be an integer")
        if v<0:
            raise ValueError("numbikes cannot be negative")
        
    @field_validator("station_arr")
    def station_uuid_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("station_arr should be an integer")
        if v<0:
            raise ValueError("station_arr cannot be negative")
        if v>20:
            raise ValueError("station_arr cannot be above 20")

>>>>>>> 952f9164f8ac0c737228f386b77471299f91964c
    
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
    