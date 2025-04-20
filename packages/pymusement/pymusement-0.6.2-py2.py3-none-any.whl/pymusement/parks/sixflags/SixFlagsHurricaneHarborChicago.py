from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborChicago(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborChicago, self).__init__()

    def getId(self):
        return 13
    def getCity(self):
        return 'Gurnee'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Chicago'

    