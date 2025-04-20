#!/usr/bin/env python
import requests
import json
import datetime
from pymusement.park import Park
from pymusement.ride import Ride

URL_TEMPLATE = 'https://api.themeparks.wiki/preview/parks/%s'
class DisneyPark(Park):

    def __init__(self):
        self._id = self.getId()
        self._url = URL_TEMPLATE % self.get_api_id()
        self.name = self.getName()
        super(DisneyPark, self).__init__()

    def getId(self):
        raise('This must be implemented in a subclass')

    def get_api_id(self):
        raise('This must be implemented in a subclass')
    
    def getName(self):
        raise('This must be implemented in a subclass')

    def _buildPark(self):
        page = self._get_page()
        for attraction in page:
            if 'type' in attraction['meta'] and attraction['meta']['type'] != 'ATTRACTION':
                continue
            self._build_attraction(attraction)

    def _build_attraction(self, attraction):
        attraction_obj = Ride()

        attraction_obj.setName(attraction['name'])
         
        if attraction['active']:
            attraction_obj.setOpen()
            attraction_obj.setTime(attraction['waitTime'])
        else:
            attraction_obj.setTime(0)
            attraction_obj.setClosed()
        attraction_obj.set_skip_line(attraction['fastPass'])
        attraction_obj.setSingleRider(attraction['meta']['singleRider'])
    
        self.addRide(attraction_obj)
    
    def _get_page(self):
        ride_link = self._url + '/waittime'
        page = requests.get(ride_link).json()
        return page


        
