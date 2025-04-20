from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsWhiteWaterAtlanta(SixFlagsPark):
    def __init__(self):
        super(SixFlagsWhiteWaterAtlanta, self).__init__()

    def getId(self):
        return 25
    def getCity(self):
        return 'Marietta'
    def getName(self):
        return 'Six Flags White Water, Atlanta'

    