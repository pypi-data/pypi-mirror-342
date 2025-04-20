from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborArlington(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborArlington, self).__init__()

    def getId(self):
        return 10
    def getCity(self):
        return 'Arlington'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Arlington'

    