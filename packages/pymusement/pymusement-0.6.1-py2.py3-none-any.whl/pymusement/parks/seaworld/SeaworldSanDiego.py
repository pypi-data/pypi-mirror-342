#!/usr/bin/env python
from pymusement.parks.seaworld.SeaworldPark import SeaworldPark

class SeaworldSanDiego(SeaworldPark):
    def __init__(self):
        super(SeaworldSanDiego, self).__init__()

    def getId(self):
        return '4325312F-FDF1-41FF-ABF4-361A4FF03443'

    def getName(self):
        return 'Seaworld San Diego'
    def getCity(self):
        return 'san-diego'