
from schema.Record import Record
from schema.Location import Location
from pydantic import BaseModel, field_validator
from schema.location import Location
class Station(BaseModel):
    
    station_uuid: int
    station_name: str
    loc: Location
    numbikes: int
    
    @field_validator("station_uuid")
    def validate_station_uuid(cls, v):
        if not(isinstance(v, int)):
            raise TypeError('Station UUID must be an integer')
        if v<0:
            raise ValueError('Station UUID cannot be negative')
        
    @field_validator("station_name")
    def station_name_not_valid(cls, v):
        if not isinstance(v, str):
            raise TypeError("station_uuid should be a string")

    @field_validator("loc")
    def station_loc_not_valid(cls, v):  
        if not isinstance(v, Location):
            raise TypeError("station_uuid should be a location")
        
    @field_validator("numbikes")
    def station_numbikes_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("numbikes should be an integer")
        if v<0:
            raise ValueError("numbikes cannot be negative")
                    
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
    