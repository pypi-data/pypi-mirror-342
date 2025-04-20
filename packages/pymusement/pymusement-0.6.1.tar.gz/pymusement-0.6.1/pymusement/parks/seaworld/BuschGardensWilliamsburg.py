#!/usr/bin/env python
from pymusement.parks.seaworld.SeaworldPark import SeaworldPark

class BuschGardensWilliamsburg(SeaworldPark):
    def __init__(self):
        super(BuschGardensWilliamsburg, self).__init__()

    def getId(self):
        return '45FE1F31-D4E4-4B1E-90E0-5255111070F2'

    def getName(self):
        return 'Busch Gardens Williamsburg'
    def getCity(self):
        return 'williamsburg'