from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborConcord(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborConcord, self).__init__()

    def getId(self):
        return 42
    def getCity(self):
        return 'Concord'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Concord'

    