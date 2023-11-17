from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from schema.location import Location
class Station(BaseModel):
    
    station_uuid: int
    station_name: str
    loc: Location
    numbikes: int
    station_arr: Optional[int] = None
    @field_validator("station_uuid")
    def validate_station_uuid(cls, v):
        if not(isinstance(v, int)):
            raise TypeError('Station UUID must be an integer')
        if v<0:
            raise ValueError('Station UUID cannot be negative')
        return v
        
    @field_validator("station_name")
    def station_name_not_valid(cls, v):
        if not isinstance(v, str):
            raise TypeError("Station name should be a string")
        return v

    @field_validator("loc")
    def station_loc_not_valid(cls, v):  
        if not isinstance(v, Location):
            raise TypeError("Station location should be a location")
        return v
        
    @field_validator("numbikes")
    def station_numbikes_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("Number of bikes should be an integer")
        if v<0:
            raise ValueError("Number of bikes cannot be negative")
        return v
                    
    @property
    def get_station_id(self) -> int:
        return self._stationId
            
    @property
    def get_station_name(self) -> str:
        return self._stationName
    
    @property
    def get_station_num_bikes(self) -> int:
        return self.__numbikes
    
    @property
    def get_station_coordinates(self) -> tuple[float]:
        return self.__loc.get_location
    
    @property
    def get_station_lon(self) -> float:
        return self.__loc.get_longitude
    
    @property
    def get_station_lat(self) -> float:
        return self.__loc.get_latitude
    
    @property
    def get_station_arr(self) -> int:
        return self._stationArr
    