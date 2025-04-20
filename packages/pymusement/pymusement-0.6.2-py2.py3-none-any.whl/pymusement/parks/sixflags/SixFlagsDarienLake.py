from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsDarienLake(SixFlagsPark):
    def __init__(self):
        super(SixFlagsDarienLake, self).__init__()

    def getId(self):
        return 45
    def getCity(self):
        return 'Darien Center'
    def getName(self):
        return 'Six Flags Darien Lake'

    