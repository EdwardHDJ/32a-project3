import website_request
import json
import math
from pathlib import Path


class JsonLoadError(Exception):
    pass

class PurpleAirData:
    def __init__(self,pm:float,lat:float,lon:float):
        self._pm = pm
        self._lat = lat
        self._lon = lon


    def get_pm(self)->float:
        return self._pm


    def get_Lat(self)->float:
        return self._lat
    

    def get_Lon(self)->float:
        return self._lon

    def get_lat_lon(self)->('lat','lon'):
        lat = str(self._lat)
        lon = str(self._lon)

        return (lat,lon)
        
    def check_in_range(self,center:('lat','lon'),distance:float)->bool:
        'check whether the sensor is in range'
        center_lat = center[0]
        center_lon = center[1]

        dlat = abs(math.radians(self._lat) - math.radians(float(center_lat)))

        dlon = abs(math.radians(self._lon) - math.radians(float(center_lon)))

        alat = (math.radians(self._lat) + math.radians(float(center_lat)))/2

        R = 3958.8

        x = dlon*math.cos(alat)
    
        d = math.sqrt(x*x+dlat*dlat)*R


        if d > distance:
            return False
        if d<= distance:
            return True
        

def round_value(value:float)->int:
    'round the value of AQI'
    if value >= int(value)+0.5:
        return int(value)+1
    elif value < int(value)+0.5:
        return int(value)
    
def calculate_AQI_value(concentration:float):
    'calculate AQI value using the formula'
    if concentration>= 0 and concentration < 12.1:  
        return round_value(0+concentration*50/12.0)
    if concentration >= 12.1 and concentration < 35.5:
        return round_value(51+(concentration-12.1)*(100-51)/(35.4-12.1))
    if concentration >= 35.5 and concentration < 55.5:
        return round_value(101+(concentration-35.5)*(150-101)/(55.4-35.5))
    if concentration >= 55.5 and concentration < 150.5 :
        return round_value(151+(concentration-55.5)*(200-151)/(150.4-55.5))
    if concentration >= 150.5 and concentration < 250.5:
        return round_value(201+(concentration-150.5)*(300-201)/(250.4-150.5))
    if concentration >= 250.5 and concentration < 350.5:
        return round_value(301+(concentration-250.5)*(400-301)/(350.4-250.5))
    if concentration >= 350.5 and concentration < 500.5:
        return round_value(401+(concentration-350.5)*(500-401)/(500.4-350.5))
    if concentration >= 500.5:
        return 501




