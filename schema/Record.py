from schema.Date import Date
from datetime import datetime
from pydantic import BaseModel, field_validator


class Record(BaseModel):
    
    station_uuid: int
    date_uuid: int
    variation: int
    
    @field_validator("station_uuid")
    def station_uuid_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("station_uuid should be an integer")
        if v<0:
            raise ValueError("station_uuid cannot be negative")
        
    @field_validator("date_uuid")
    def date_uuid_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("date_uuid should be an integer")
        if v<0:
            raise ValueError("date_uuid cannot be negative")
        
    @field_validator("variation")
    def variation_not_valid(cls, v):
        if not isinstance(v, int):
            raise TypeError("variation should be an integer")
        if v<0:
            raise ValueError("variation cannot be negative")
            
    @property
    def getStationUuid(self) -> int:
        return self.station_uuid

    @property
    def getDateUuid(self) -> int:
        return self.date_uuid

    @property
    def getVariation(self) -> int:
        return self.variation

    
    