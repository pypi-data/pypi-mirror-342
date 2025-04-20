from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsMexico(SixFlagsPark):
    def __init__(self):
        super(SixFlagsMexico, self).__init__()

    def getId(self):
        return 28
    def getCity(self):
        return 'Ciudad de México'
    def getName(self):
        return 'Six Flags México'

    
