from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsGreatAmerica(SixFlagsPark):
    def __init__(self):
        super(SixFlagsGreatAmerica, self).__init__()

    def getId(self):
        return 7
    def getCity(self):
        return 'Gurnee'
    def getName(self):
        return 'Six Flags Great America'

    