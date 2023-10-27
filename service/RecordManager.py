from database.DAORecord import DAORecord

class RecordManager():
    #need to see how to compute the min (mean, numbers of Records etc... )
    def getMinFrequentationStation(date_start : datetime, date_end : datetime) -> int :
        
        variation= DAORecord.getVargroupSationByDate(date_start, date_end)
        lessfrequented_station = min(variation, key = lambda t: t[1])[0]
        return lessfrequented_station

    def getMaxFrequentationArrondissement(date_start : datetime, date_end : datetime) -> int : 
        variation= DAORecord.getVargroupArrByDate(date_start, date_end)
        lessfrequented_station = max(variation, key = lambda t: t[1])[0]
        return lessfrequented_station
    
    