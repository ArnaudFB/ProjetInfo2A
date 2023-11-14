from pydantic import BaseModel, field_validator
from typing import Tuple

class Location(BaseModel):
    
    lat: float
    lon: float
    
    @property
    def get_location(self):
        return (self.lat, self.lon)
    
    @property
    def get_latitude(self):
        return self.lat
    
    @property
    def get_longitude(self):
        return self.lon

