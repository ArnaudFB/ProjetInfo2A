from pydantic import BaseModel, field_validator


class Location(BaseModel):
    lat: float
    lon: float
    @property
    def getLocation(self):
        return (self.lat, self.lon)

    @property
    def getLatitude(self):
        return self.lat

    @property
    def getLongitude(self):
        return self.lon
