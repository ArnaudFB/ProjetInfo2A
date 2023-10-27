from datetime import datetime

class Date:
    
    def __init__(self, date: datetime):
        self.date = date
    
    @property
    def get_date(self):
        return self.date
    
    def is_superior(self, date2) -> bool:
        return (self.date >= date2)
    
    def is_inferior(self, date2) -> bool:
        return (self.date <= date2)
    