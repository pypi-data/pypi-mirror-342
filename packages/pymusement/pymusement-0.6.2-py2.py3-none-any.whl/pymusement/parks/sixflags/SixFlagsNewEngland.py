from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsNewEngland(SixFlagsPark):
    def __init__(self):
        super(SixFlagsNewEngland, self).__init__()

    def getId(self):
        return 20
    def getCity(self):
        return 'Agawam'
    def getName(self):
        return 'Six Flags New England'

    