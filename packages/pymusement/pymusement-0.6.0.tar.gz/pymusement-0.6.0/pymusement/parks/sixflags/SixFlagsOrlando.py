from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsOrlando(SixFlagsPark):
    def __init__(self):
        super(SixFlagsOrlando, self).__init__()

    def getId(self):
        return 1234
    def getCity(self):
        return 'Orlando'
    def getName(self):
        return 'Six Flags Orlando'

    