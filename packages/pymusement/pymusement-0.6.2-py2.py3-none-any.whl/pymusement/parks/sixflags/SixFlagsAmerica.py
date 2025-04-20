from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsAmerica(SixFlagsPark):
    def __init__(self):
        super(SixFlagsAmerica, self).__init__()

    def getId(self):
        return 14
    def getCity(self):
        return 'Bowie'
    def getName(self):
        return 'Six Flags America'

    