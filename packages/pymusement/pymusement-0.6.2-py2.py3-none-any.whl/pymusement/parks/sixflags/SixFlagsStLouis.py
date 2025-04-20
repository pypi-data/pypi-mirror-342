from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsStLouis(SixFlagsPark):
    def __init__(self):
        super(SixFlagsStLouis, self).__init__()

    def getId(self):
        return 3
    def getCity(self):
        return 'Eureka'
    def getName(self):
        return 'Six Flags St. Louis'

    