from pydantic import BaseModel, field_validator
class Record(BaseModel):
    
    station_uuid: int
    date_uuid: int
    variation: int
    
    @field_validator("station_uuid")
    def station_uuid_not_valid(cls, v):
        if v<0:
            raise ValueError("station_uuid cannot be negative")
        return v
        
    @field_validator("date_uuid")
    def date_uuid_not_valid(cls, v):
        if v<0:
            raise ValueError("date_uuid cannot be negative")
        return v
    
    @field_validator("variation")
    def variation_not_valid(cls, v):
        if v<0:
            raise ValueError("variation cannot be negative")
        return v
            
    @property
    def get_station_uuid(self) -> int:
        return self.station_uuid

    @property
    def get_date_uuid(self) -> int:
        return self.date_uuid

    @property
    def get_variation(self) -> int:
        return self.variation
    