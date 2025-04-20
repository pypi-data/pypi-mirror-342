from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsFrontierCity(SixFlagsPark):
    def __init__(self):
        super(SixFlagsFrontierCity, self).__init__()

    def getId(self):
        return 43
    def getCity(self):
        return 'Oklahoma City'
    def getName(self):
        return 'Six Flags Frontier City'

    