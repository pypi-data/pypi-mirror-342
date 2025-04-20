from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsOverGeorgia(SixFlagsPark):
    def __init__(self):
        super(SixFlagsOverGeorgia, self).__init__()

    def getId(self):
        return 2
    def getCity(self):
        return 'Austell'
    def getName(self):
        return 'Six Flags Over Georgia'



