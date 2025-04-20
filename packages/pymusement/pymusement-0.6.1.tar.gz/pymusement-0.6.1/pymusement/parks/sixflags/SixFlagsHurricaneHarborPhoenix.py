from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborPhoenix(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborPhoenix, self).__init__()

    def getId(self):
        return 46
    def getCity(self):
        return 'Glendale'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Phoenix'

    