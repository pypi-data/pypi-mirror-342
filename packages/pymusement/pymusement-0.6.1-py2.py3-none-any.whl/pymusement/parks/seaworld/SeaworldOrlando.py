#!/usr/bin/env python
from pymusement.parks.seaworld.SeaworldPark import SeaworldPark

class SeaworldOrlando(SeaworldPark):
    def __init__(self):
        super(SeaworldOrlando, self).__init__()

    def getId(self):
        return 'AC3AF402-3C62-4893-8B05-822F19B9D2BC'

    def getName(self):
        return 'Seaworld Orlando'
    def getCity(self):
        return 'orlando'
park = SeaworldOrlando()
