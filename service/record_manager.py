from database.dao_record import DAORecord
from datetime import datetime

class RecordManager():
    #need to see how to compute the min (mean, numbers of Records etc... )
    def get_min_frequentation_station(date_start : datetime, date_end : datetime) -> int :
        
        variation= DAORecord.get_var_groupstation_bydate(date_start, date_end)
        lessfrequented_station = min(variation, key = lambda t: t[1])[0]
        return lessfrequented_station

    def get_max_frequentation_arrondissement(date_start : datetime, date_end : datetime) -> int : 
        variation= DAORecord.get_var_grouparr_bydate(date_start, date_end)
        morefrequented_station = max(variation, key = lambda t: t[1])[0]
        return morefrequented_station