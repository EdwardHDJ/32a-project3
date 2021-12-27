import website_request
from pathlib import Path
import json
import PurpleAir
import time
class JsonLoadError(Exception):
    pass
class FileNotFoundError1(Exception):
    pass
class FowardNominatimWebApi:
    def __init__(self,search_content:str):
        self._search_content =search_content

    def search_content_and_return_result(self)->(str,str):
        'forward Nominatim decoding'
        search_url = website_request.search_place_by_name(self._search_content)
        try:
            data_text = website_request.get_file_from_url_nominatim(search_url)
        except website_request.ConnectionErrorNot200:
            raise website_request.ConnectionErrorNot200
        except website_request.NoConnectionError:
            raise website_request.NoConnectionError
        try:
            place_dict = json.loads(data_text)
        except json.JSONDecodeError:
            print('FAILED')
            print('Status Code', 200,'url:',search_url)
            print('FORMAT')
            raise JsonLoadError
        
        return (place_dict[0]['lat'],place_dict[0]['lon'])


class ReverseNominatimWebApi:
    def __init__(self,search_content:(str,str)):
        self._search_content = search_content

    def search_content_and_return_result(self)->str:
        'reverse nominatim decoding'
        search_url = website_request.search_place_by_address(self._search_content)
        try:
            data_text =website_request.get_file_from_url_nominatim(search_url)
        except website_request.ConnectionErrorNot200:
            raise website_request.ConnectionErrorNot200
        except website_request.NoConnectionError:
            raise website_request.NoConnectionError

        try:
            place_dict = json.loads(data_text)
        except json.JSONDecodeError:
            print('FAILED')
            print('Status Code', 200,'url:',search_url)
            print('FORMAT')
            raise JsonLoadError

        time.sleep(1)

        return place_dict['display_name']

class PurpleAirApi:
    def search_content_and_return_result(self)->['data']:
        'get sensor datalist from the webiste'
        try:
            data_text = website_request.get_file_from_url('https://www.purpleair.com/data.json')
        except website_request.ConnectionErrorNot200:
            raise website_request.ConnectionErrorNot200
        except website_request.NoConnectionError:
            raise website_request.NoConnectionError
                
        try:
            PurpleAir_datadict = json.loads(data_text)
        except json.JSONDecodeError:
            print('FAILED')
            print('Status Code',200,'url: https://www.purpleair.com/data.json')
            print('FORMAT')
            raise JsonLoadError
        
        PurpleAir_datalist = []
        
        for sensor_data in PurpleAir_datadict['data']:
            if sensor_data[1] != None and sensor_data[27] != None and sensor_data[28] != None and sensor_data[4] != None \
               and sensor_data[25] != None and sensor_data[4] < 3600 and sensor_data[25] == 0:
                PurpleAir_datalist.append(PurpleAir.PurpleAirData(sensor_data[1],sensor_data[27],\
                                                            sensor_data[28]))
        return PurpleAir_datalist

class ForwardNominatimFile:
    def __init__(self,path:Path):
        self._file_location = path

    def search_content_and_return_result(self)->str:
        'get the address description from website'
        the_file = None
        try:
            the_file = open(self._file_location,encoding = 'utf-8')
            content = the_file.read()
        except FileNotFoundError:
            print('FAILED')
            print('path:',self._file_location)
            print('MISSING')
            raise FileNotFoundError1
        finally:
            if the_file != None:
                the_file.close()
        
        
        try:
            place_dict = json.loads(content)
        except json.JSONDecodeError:
            print('FAILED')
            print('path:',self._file_location)
            print('FORMAT')
            raise JsonLoadError
        
        return place_dict['display_name']

class ForwardNominatimFileCenter:
    def __init__(self,path:Path):
        self._file_location = path

    def search_content_and_return_result(self)->str:
        'get address name from file'
        the_file = None
        try:
            the_file = open(self._file_location,encoding = 'utf-8')
            content = the_file.read()
        except FileNotFoundError:
            print('FAILED')
            print('url:',search_url)
            print('MISSING')
            raise FileNotFoundError1
        finally:
            if the_file != None:
                the_file.close()
        
        
        try:
            place_dict = json.loads(content)
        except json.JSONDecodeError:
            print('FAILED')
            print('path:',self._file_location)
            print('FORMAT')
            raise JsonLoadError
        
        return place_dict[0]['display_name']

class ReverseNominatimFileCenter:
    def __init__(self,path:Path):
        self._file_location = path

    def search_content_and_return_result(self)->('lat','lon'):
        'get address latitude and lontitude than put them into a tuple'
        the_file = None
        try:
            the_file = open(self._file_location,encoding = 'utf-8')
            content = the_file.read()
        except FileNotFoundError:
            print('FAILED')
            print('path:',self._file_location)
            print('MISSING')
            raise FileNotFoundError1
        finally:
            if the_file != None:
                the_file.close()
        
        
        try:
            place_dict = json.loads(content)
        except json.JSONDecodeError:
            print('FAILED')
            print('path:',self._file_location)
            print('FORMAT')
            raise JsonLoadError

        return (place_dict[0]['lat'],place_dict[0]['lon'])

class ReverseNominatimFile:
    def __init__(self,path:Path):
        self._file_location = path

    def search_content_and_return_result(self)->('lat','lon'):
        'get latitude and lontitude from a file'
        the_file = None
        try:  
            the_file = open(self._file_location,encoding = 'utf-8')
            content = the_file.read()
        except FileNotFoundError:
            print('FAILED')
            print('path:',self._file_location)
            print('MISSING')
            raise FileNotFoundError1
        finally:
            if the_file != None:
                the_file.close()
            
        try:
            place_dict = json.loads(content)
        except json.JSONDecodeError:
            print('FAILED')
            print('path:',self._file_location)
            print('FORMAT')
            raise JsonLoadError

        return (place_dict['lat'],place_dict['lon'])

class PurpleAirFile:
    def __init__(self,path:Path):
        self._file_location = path

    def search_content_and_return_result(self)->['data']:
        'get purpleair data from a file'
        the_file = None
        try:
            the_file = open(self._file_location,encoding = 'utf-8')
            data_text = the_file.read()
        except FileNotFoundError:
            print('FAILED')
            print('path:',self._file_location)
            print('MISSING')
            raise FileNotFoundError1
        finally:
            if the_file != None:
                the_file.close()
            
        try:
            PurpleAir_datadict = json.loads(data_text)
        except json.JSONDecodeError:
            print('FAILED')
            print('path:',self._file_location)
            print('FORMAT')
            raise JsonLoadError
        
        PurpleAir_datalist = []
        
        for sensor_data in PurpleAir_datadict['data']:
            if sensor_data[1] != None and sensor_data[27] != None and sensor_data[28] != None and sensor_data[4] != None\
               and sensor_data[25] != None and sensor_data[4] < 3600 and sensor_data[25] == 0:
                PurpleAir_datalist.append(PurpleAir.PurpleAirData(sensor_data[1],sensor_data[27],\
                                                            sensor_data[28]))
        return PurpleAir_datalist



 





