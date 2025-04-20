from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborOklahomaCity(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborOklahomaCity, self).__init__()

    def getId(self):
        return 44
    def getCity(self):
        return 'Oklahoma City'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Oklahoma City'

    