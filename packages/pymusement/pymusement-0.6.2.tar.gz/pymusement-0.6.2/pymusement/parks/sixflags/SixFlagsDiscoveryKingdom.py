from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsDiscoveryKingdom(SixFlagsPark):
    def __init__(self):
        super(SixFlagsDiscoveryKingdom, self).__init__()

    def getId(self):
        return 17
    def getCity(self):
        return 'Vallejo'
    def getName(self):
        return 'Six Flags Discovery Kingdom'

    