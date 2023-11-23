from pydantic import BaseModel, Field, field_validator
from datetime import datetime
class Date(BaseModel):
    
    date: datetime = Field(default=datetime.now().replace(second=0))
    @field_validator("date")
    def date_cant_be_in_future(cls, v):
        if v > datetime.now():
            raise ValueError("Date can't be in the future.")

        return v
    
    @property
    def get_date(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')
