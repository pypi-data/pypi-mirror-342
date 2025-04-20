from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsGreatAdventure(SixFlagsPark):
    def __init__(self):
        super(SixFlagsGreatAdventure, self).__init__()

    def getId(self):
        return 5
    def getCity(self):
        return 'Jackson'
    def getName(self):
        return 'Six Flags Great Adventure'

    