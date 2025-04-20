from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborLosAngeles(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborLosAngeles, self).__init__()

    def getId(self):
        return 11
    def getCity(self):
        return 'Valencia'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Los Angeles'

    