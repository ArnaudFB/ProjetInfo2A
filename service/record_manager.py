from database.dao_record import DAORecord
from datetime import datetime
class RecordManager():
    
    def get_min_frequentation_station(date_start : datetime, date_end : datetime, cutting : str ) -> int :
        number_d = (date_end - date_start).days
        number_w = number_d // 7
        number_m = number_d // 30.44 #durée moyenne d'un m
        number_h = (number_d.days * 24)

        variation= DAORecord.get_var_groupstation_bydate(date_start, date_end)

        less_frequented_station = min(variation, key = lambda t: t[1]/globals()['number_{}'.format(cutting)])[0]
        return less_frequented_station

    def get_max_frequentation_arrondissement(date_start : datetime, date_end : datetime, cutting : str) -> int : 
        number_d = (date_end - date_start).days
        number_w = number_d // 7
        number_m = number_d // 30.44 #durée moyenne d'un m
        number_h = (number_d.days * 24)
        variation= DAORecord.get_var_grouparr_bydate(date_start, date_end)
        more_frequented_station = max(variation, key = lambda t: t[1]/globals()['number_{}'.format(cutting)])[0]
        return more_frequented_station


