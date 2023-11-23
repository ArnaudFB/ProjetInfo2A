from pydantic import BaseModel, field_validator, validator
from typing import Optional
from schema.location import Location
class Station(BaseModel):
    
    station_uuid: int
    station_name: str
    loc: Location
    numbikes: int
    station_arr: Optional[int] = None

    @validator('station_arr', pre=True, always=True)
    def set_station_arr(cls, v, values):
        station_uuid = str(values.get('station_uuid', ''))  # Get station_uuid from values
        if station_uuid:
            arr_num = int(station_uuid[:-3])
            if arr_num <= 20:
                return arr_num
        return None
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
        return self.station_uuid
            
    @property
    def get_station_name(self) -> str:
        return self.station_name
    
    @property
    def get_station_num_bikes(self) -> int:
        return self.numbikes
    
    @property
    def get_station_coordinates(self) -> tuple[float]:
        return self.loc.get_location
    
    @property
    def get_station_lon(self) -> float:
        return self.loc.get_longitude
    
    @property
    def get_station_lat(self) -> float:
        return self.loc.get_latitude
    
    @property
    def get_station_arr(self) -> int:
        return self.station_arr
    