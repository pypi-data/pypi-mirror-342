#!/usr/bin/env python
import requests
from pymusement.park import Park
from pymusement.ride import Ride
from pymusement.show import Show
import datetime

PARK_URL = 'https://public.api.seaworld.com/v1/park/{0}/'
RIDE_URL = 'https://public.api.seaworld.com/v1/park/{0}/availability'
#SHOW_URL = 'https://seas.te2.biz/v1/rest/venue/{0}/shows/{1}'

class SeaworldPark(Park):
        
    def __init__(self):
        super(SeaworldPark, self).__init__()
        self._park_url = PARK_URL.format(self.getId())
        self._ride_url = RIDE_URL.format(self.getId())

    def _buildPark(self):
        parsed_page = requests.get(self._park_url).json()
        wait_times = requests.get(self._ride_url).json()
        times = wait_times['WaitTimes']
        wait_times = { x['Id']:x['Minutes'] for x in times }
        ride_status = { x['Id']:x['Status'] for x in times }
        hour_page = parsed_page['open_hours']
        for date in hour_page:
                open_time, close_time = datetime.datetime.fromisoformat(date['opens_at'][:-1]), datetime.datetime.fromisoformat(date['closes_at'][:-1])

                if open_time < datetime.datetime.now() < close_time:
                    self.set_open()
                    self.park_hours = open_time.time().strftime('%r') + ' ' + close_time.time().strftime('%r')
                    break
                else:
                    self.set_closed()
                    self.park_hours = open_time.time().strftime('%r') + ' ' + close_time.time().strftime('%r')
                    break
        
        for ride in parsed_page['POIs']['Rides']:
            try:
                ride.update({'WaitTime':wait_times[ride['Id']]})
            except KeyError:
                ride.update({'WaitTime':-1})
            try:
                ride.update({'Status':ride_status[ride['Id']]})
            except KeyError:
                ride.update({'Status':''})
            self._make_attraction(ride)
    def _make_attraction(self, ride):
        # Create dictionary with attraction information
        attraction = Ride()
        attraction.setName(ride['Name'])
        
       # if not self.is_Open:
       #     attraction.setTime(0)
       #     attraction.setClosed()
       #     self.addRide(attraction)
       #     return
        
        if ride['WaitTime'] is None:
            attraction.setClosed()
        else:
            attraction.setOpen() 
        
        if ride['WaitTime'] == -1:
            attraction.setClosed()
            attraction.setTime(-1)
            attraction.setStatus(ride['Status'])
        else:
            attraction.setTime(ride['WaitTime'])
            attraction.setStatus('Operating')
            
            
        self.addRide(attraction)
        

 
