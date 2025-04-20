from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsMagicMountain(SixFlagsPark):
    def __init__(self):
        super(SixFlagsMagicMountain, self).__init__()

    def getId(self):
        return 6
    def getCity(self):
        return 'Valencia'
    def getName(self):
        return 'Six Flags Magic Mountain'

    