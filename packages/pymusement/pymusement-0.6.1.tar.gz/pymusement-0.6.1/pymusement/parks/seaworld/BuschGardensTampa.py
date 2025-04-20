#!/usr/bin/env python
from pymusement.parks.seaworld.SeaworldPark import SeaworldPark

class BuschGardensTampa(SeaworldPark):
    def __init__(self):
        super(BuschGardensTampa, self).__init__()

    def getId(self):
        return 'C001866B-555D-4E92-B48E-CC67E195DE96'

    def getName(self):
        return 'Busch Gardens Tampa'
        
    def getCity(self):
        return 'tampa'
