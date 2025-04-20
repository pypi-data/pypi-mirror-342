#!/usr/bin/env python
from pymusement.parks.seaworld.SeaworldPark import SeaworldPark

class SeaworldSanAntonio(SeaworldPark):
    def __init__(self):
        super(SeaworldSanAntonio, self).__init__()

    def getId(self):
        return 'F4040D22-8B8D-4394-AEC7-D05FA5DEA945'

    def getName(self):
        return 'Seaworld San Antonio'
    def getCity(self):
        return 'san-antonio'