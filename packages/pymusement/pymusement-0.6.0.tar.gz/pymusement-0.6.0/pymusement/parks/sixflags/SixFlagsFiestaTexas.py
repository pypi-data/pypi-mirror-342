from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class SixFlagsFiestaTexas(SixFlagsPark):
    def __init__(self):
        super(SixFlagsFiestaTexas, self).__init__()

    def getId(self):
        return 8
    def getCity(self):
        return 'San Antonio'
    def getName(self):
        return 'Six Flags Fiesta Texas'

    