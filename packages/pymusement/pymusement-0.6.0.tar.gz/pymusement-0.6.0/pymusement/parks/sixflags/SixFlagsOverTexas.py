from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsOverTexas(SixFlagsPark):
    def __init__(self):
        super(SixFlagsOverTexas, self).__init__()

    def getId(self):
        return 1
    def getCity(self):
        return 'Arlington'
    def getName(self):
        return 'Six Flags Over Texas'

    