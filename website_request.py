import urllib.request
import urllib.parse
import urllib.error
import time
BASE_URL = 'https://nominatim.openstreetmap.org/'

class ConnectionErrorNot200(Exception):
    pass
class NoConnectionError(Exception):
    pass

def get_file_from_url(url:str)->str:
    'get file from the url and raise exception if there is an error'

    try:
        response = None
        
        request = urllib.request.Request(url)

        response = urllib.request.urlopen(request)

        data_text = response.read().decode(encoding = 'utf-8')
        
    except urllib.error.HTTPError as e:
        print('FAILED')
        print('Status code: {}'.format(e.code),'Url:',url)
        print('NOT 200')
        raise ConnectionErrorNot200

    except urllib.error.URLError :
        print('FAILED')
        print('Url:',url)
        print('NETWORK')
        raise NoConnectionError

    finally:
        if response != None:
            response.close()
    
    return data_text


    
##get_file_from_url('https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/')
def get_file_from_url_nominatim(url:str)->str:
    'get file special for nominatim, with a personal header'

    try:
        response = None
        
        request = urllib.request.Request(url,headers = { 'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/dejianh'})

        response = urllib.request.urlopen(request)

        data_text = response.read().decode(encoding = 'utf-8')


    except urllib.error.HTTPError as e:
        print('FAILED')
        print('Status code: {}'.format(e.code),'Url:',url)
        print('NOT 200')
        raise ConnectionErrorNot200

    except urllib.error.URLError:
        print('FAILED')
        print('Url:',url)
        print('NETWORK')
        raise NoConnectionError

    finally:
        if response != None:
            response.close()

    return data_text


    

def search_place_by_name(user_input:str)->str:
    'construct the searching url'
    url = urllib.parse.urlencode([('q', user_input),('format','json'),('addressdetail',1),('limit',1)])
    return BASE_URL + 'search?'+ url



def search_place_by_address(lat_ton:('lat','lon')):
    'construct the searching url'
    lat = lat_ton[0]
    lon = lat_ton[1]
    url = urllib.parse.urlencode([('format' , 'json'),('lat',lat),('lon',lon)])
    return BASE_URL + 'reverse?' + url


