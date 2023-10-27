from datetime import datetime

class Date:
    
    def __init__(self, date: datetime):
        self.date = date
    
    @property
    def getDate(self):
        return self.date
    
    def isSuperior(self, date2) -> bool:
        return (self.date >= date2)
    
    def isInferior(self, date2) -> bool:
        return (self.date <= date2)
    