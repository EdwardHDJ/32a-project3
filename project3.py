import PurpleAir
import math
import website_request
from pathlib import Path
import api_tools

def check_line(line:str,expected:str)->bool:
    'check what the line start with'
    if line.startswith(expected):
        return True
    
    return False

def get_location_from_line(line:str)->str:
    'put the location in the line into a string'
    location = line[17:]

    return location

def get_path_from_line(line:str)->str:
    'put the path in the line into a string'
    path = line[12:]

    return path

    
#what if lat or lon is equal to zero
#check direction
def convert_lat_lon(lat_lon:tuple)->str:
    'covert lat and lon tuple to a new string'
    lat = lat_lon[0]

    lon = lat_lon[1]

    if float(lat) > 0:
        lat = lat+'/N'
    elif float(lat) < 0:
        lat = lat[1:]+'/S'

    if float(lon) > 0:
        lon = lon+'/E'
    elif float(lon)<0:
         lon = lon[1:]+'/W'

    return lat +' '  + lon


'''
Test Case:
CENTER NOMINATIM Bren Hall, Irvine, CA
RANGE 30
THRESHOLD 100
MAX 5
AQI PURPLEAIR
REVERSE NOMINATIM

CENTER FILE nominatim_center.json
RANGE 30
THRESHOLD 50
MAX 3
AQI FILE purpleair.json
REVERSE FILES nominatim_reverse1.json nominatim_reverse2.json nominatim_reverse3.json
'''
def run():
    try:
        output_string = ''
        first_line = input()
        second_line = input()
        third_line = input()
        forth_line = input()
        fifth_line = input()
        sixth_line = input()

        search_range = int(second_line[6:])

        threshold = int(third_line[10:])

        max_number = int(forth_line[4:])

        in_range_datalist = []

        final_datalist = []

        output_datalist = []

        
        if check_line(first_line,'CENTER NOMINATIM') == True:
            location = get_location_from_line(first_line)
            location_tuple = api_tools.FowardNominatimWebApi(location).search_content_and_return_result()
            location_lat_lon = convert_lat_lon(location_tuple)
            output_string += 'CENTER '+ location_lat_lon+'\n'

        elif check_line(first_line,'CENTER FILE') == True:
            path = Path(get_path_from_line(first_line))
            location_tuple = api_tools.ReverseNominatimFileCenter(path).search_content_and_return_result()
            location_lat_lon = convert_lat_lon(location_tuple)
            output_string += 'CENTER '+ location_lat_lon+'\n'

        
        

        if check_line(fifth_line,'AQI PURPLEAIR')== True:
            PurpleAir_datalist = api_tools.PurpleAirApi().search_content_and_return_result()

        if check_line(fifth_line,'AQI FILE')== True:
            path = Path(fifth_line[9:])
            PurpleAir_datalist = api_tools.PurpleAirFile(path).search_content_and_return_result()

        for data in PurpleAir_datalist:
            if data.check_in_range(location_tuple,search_range) == True:
                in_range_datalist.append(data)
                

        sorted_datalist = sorted(in_range_datalist,key =  lambda data :data._pm,reverse = True)
        
        for data in sorted_datalist:
            PurpleAir_AQI_value = PurpleAir.calculate_AQI_value(data.get_pm())
            if PurpleAir_AQI_value >= threshold:
                final_datalist.append(data)
        
        index = 0
        
        for data in final_datalist:
            if index == max_number:
                break
            output_datalist.append(data)
            index += 1
        
        if check_line(sixth_line,'REVERSE NOMINATIM'):
            for data in output_datalist:
                PurpleAir_AQI_value = PurpleAir.calculate_AQI_value(data.get_pm())
                output_string += 'AQI ' + str(PurpleAir_AQI_value)+'\n'
                output_string += convert_lat_lon(data.get_lat_lon())+'\n'
                output_string += api_tools.ReverseNominatimWebApi((data.get_Lat(),data.get_Lon())).search_content_and_return_result()+'\n'
                index += 1
        
        elif check_line(sixth_line,'REVERSE FILES'):
            file_pathlist = sixth_line[14:].split()
            index = 0
            for path in file_pathlist:
                if index == len(output_datalist):
                    break
                path = Path(path)
                output_string += 'AQI ' + str(PurpleAir.calculate_AQI_value(output_datalist[index].get_pm()))+'\n'
                output_string += convert_lat_lon(output_datalist[index].get_lat_lon())+'\n'
                output_string += api_tools.ForwardNominatimFile(path).search_content_and_return_result()+'\n'
                index += 1
                
        print(output_string)

    except website_request.NoConnectionError:
        pass
        
    except website_request.ConnectionErrorNot200:
        pass

    except api_tools.JsonLoadError:
        pass

    except api_tools.FileNotFoundError1:
        pass
    

if __name__ == '__main__':
    run()

