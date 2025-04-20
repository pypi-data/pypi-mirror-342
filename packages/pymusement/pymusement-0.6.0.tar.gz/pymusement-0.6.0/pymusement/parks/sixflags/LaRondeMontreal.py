from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class LaRondeMontreal(SixFlagsPark):
    def __init__(self):
        super(LaRondeMontreal, self).__init__()

    def getId(self):
        return 29
    def getCity(self):
        return 'Montreal'
    def getName(self):
        return 'La Ronde, Montreal'

    