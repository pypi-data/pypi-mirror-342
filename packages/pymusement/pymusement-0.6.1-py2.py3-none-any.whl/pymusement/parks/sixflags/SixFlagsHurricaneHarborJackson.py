from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborJackson(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborJackson, self).__init__()

    def getId(self):
        return 23
    def getCity(self):
        return 'Jackson'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Jackson'

    