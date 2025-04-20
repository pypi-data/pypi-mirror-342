import requests
import datetime
from pymusement.park import Park
from pymusement.ride import Ride

SHARED_HEADERS = {
    'Accept'                          : 'application/json',
    'Accept-Language'                 : 'en-US',
    'X-UNIWebService-AppVersion'      : '1.2.1',
    'X-UNIWebService-Platform'        : 'Android',
    'X-UNIWebService-PlatformVersion' : '4.4.2',
    'X-UNIWebService-Device'          : 'samsung SM-N9005',
    'X-UNIWebService-ServiceVersion'  : '1',
    'User-Agent'                      : 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-N9005 Build/KOT49H)',
    'Connection'                      : 'keep-alive',
    'Accept-Encoding'                 : 'gzip'
  }

WAIT_URL = 'https://api.sixflags.net/mobileapi/v1/park/{0}/rideStatus'

META_URL = 'https://api.sixflags.net/mobileapi/v1/park/{0}/ride'

HOURS_URL = 'https://api.sixflags.net/mobileapi/v1/park/{0}/hours'


class SixFlagsPark(Park):
    def __init__(self):
        super(SixFlagsPark, self).__init__()
        self.ride_url = WAIT_URL.format(self.getId())
        self.info_url = META_URL.format(self.getId())
        self.hour_url = HOURS_URL.format(self.getId())
    def getId(self):
        raise('This must be implemented in a sub class')
        
    def _buildPark(self):
        token = self._get_token()
        ride_page = self._get_request(token, self.ride_url)
        metadata_page = self._get_request(token, self.info_url)
        hour_page = self._get_request(token,self.hour_url)
            
        ride_info = {x['rideId']:x for x in metadata_page['rides']}
        
        try:
            hours = -1
            for time in hour_page['operatingHours']:
                if datetime.datetime.fromisoformat(time['operatingDate']).date() == datetime.date.today():

                    hours = time
                    break
            if hours == -1:
                self.set_closed()
                self.park_hours = 'Closed'
            else:
                open_time, close_time = datetime.datetime.fromisoformat(hours['open']), datetime.datetime.fromisoformat(hours['close'])
                self.park_hours = open_time.time().strftime('%r') + ' ' + close_time.time().strftime('%r')
               
                if open_time < datetime.datetime.now() < close_time:
                    self.set_open()
                    self.park_hours = open_time.time().strftime('%r') + ' ' + close_time.time().strftime('%r')
                
                else:
                    self.set_closed()
                    self.park_hours = open_time.time().strftime('%r') + ' ' + close_time.time().strftime('%r')
                
        except IndexError:
            self.set_closed()
            self.park_hours = 'Closed'
            
            
               
        
        for ride in ride_page['rideStatuses']:
            self._make_attraction(ride,ride_info[ride['rideId']])

    def _make_attraction(self, ride, meta):
        attraction = Ride()
        attraction.setName(meta['name'])
        attraction.setStatus(meta['status'])
        
        #Check if Park is Open
        if not self.is_Open:
            attraction.setTime(0)
            attraction.setClosed()
            attraction.set_skip_line(meta['isFlashPassEligible'])
            self.addRide(attraction)
            return

        if meta['status'] == 'AttractionStatusOpen':
            attraction.setOpen()
        else:
            attraction.setClosed()
        try:
            int(ride['waitTime'])
        except ValueError:
            ride['waitTime'] = ''.join(c for c in ride['waitTime'] if c.isdigit())
        except TypeError:
            if ride['waitTime']: raise ValueError
            else: ride['waitTime'] = 0
        attraction.setTime(ride['waitTime'])
        attraction.set_skip_line(meta['isFlashPassEligible'])

        
        
        
        self.addRide(attraction)


    def _get_request(self, token, url):
        headers={'Authorization': 'Bearer '+ token}
        r = requests.get(url, headers=headers)
        return r.json()

    def _get_token(self):
        headers = {
            'Authorization':'Basic MEExQ0RGNjctMjQ3Ni00Q0IyLUFCM0ItMTk1MTNGMUY3NzQ3Ok10WEVKU0hMUjF5ekNTS3FBSVZvWmt6d2ZDUUFUNEIzTVhIZ20rZVRHU29xSkNBRDRXUHlIUnlYK0drcFZYSHJBNU9ZdUFKRHYxU3p3a3UxWS9sM0Z3PT0='
        }
        data={"grant_type":"client_credentials","scope":"mobileApp"}
        r = requests.post('https://api.sixflags.net/Authentication/identity/connect/token', headers=headers,data=data)
        return r.json()['access_token']
