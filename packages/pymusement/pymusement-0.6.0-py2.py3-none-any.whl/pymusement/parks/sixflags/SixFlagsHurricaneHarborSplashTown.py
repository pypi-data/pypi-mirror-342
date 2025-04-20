from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsHurricaneHarborSplashTown(SixFlagsPark):
    def __init__(self):
        super(SixFlagsHurricaneHarborSplashTown, self).__init__()

    def getId(self):
        return 47
    def getCity(self):
        return 'Spring'
    def getName(self):
        return 'Six Flags Hurricane Harbor, SplashTown'

    