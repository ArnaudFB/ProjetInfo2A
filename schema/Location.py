from pydantic import BaseModel, field_validator

class Location(BaseModel):
    
    lat:float 
    lon:float
    
    @field_validator("lat")
    def lat_must_be_valid(cls, v):
        if not(isinstance(v, float)):
            raise TypeError("latitude must be a float")
        if abs(v)>90:
            raise ValueError("latitude should be between -90 and 90")
            
            
    @field_validator("lon")
    def lat_must_be_valid(cls, v):
        if not(isinstance(v, float)):
            raise TypeError("longitude must be a float")
        if abs(v)>180:
            raise ValueError("longitude should be between -180 and 180")
    
    @property
    def getLocation(self):
        return (self.lat, self.lon)
    
    @property
    def getLatitude(self):
        return self.lat
    
    @property
    def getLongitude(self):
        return self.lon
