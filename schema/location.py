from pydantic import BaseModel, field_validator

class Location(BaseModel):
    lat: float
    lon: float
    @field_validator("lat")
    def lat_must_be_valid(cls, v):
        if not (isinstance(v, float)):
            raise TypeError("latitude must be a float")
        if abs(v) > 90:
            raise ValueError("latitude should be between -90 and 90")
        return v

    @field_validator("lon")
    def lon_must_be_valid(cls, v):
        if not (isinstance(v, float)):
            raise TypeError("longitude must be a float")
        if abs(v) > 180:
            raise ValueError("longitude should be between -180 and 180")
        return v
    @property
    def get_location(self):
        return (self.lat, self.lon)

    @property
    def get_latitude(self):
        return self.lat

    @property
    def get_longitude(self):
        return self.lon
