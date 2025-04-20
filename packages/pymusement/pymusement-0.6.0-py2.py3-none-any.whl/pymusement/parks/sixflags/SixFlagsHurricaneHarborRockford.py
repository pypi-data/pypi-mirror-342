from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborRockford(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborRockford, self).__init__()

    def getId(self):
        return 48
    def getCity(self):
        return 'Cherry Valley'
    def getName(self):
        return 'Six Flags Hurricane Harbor, Rockford'

    