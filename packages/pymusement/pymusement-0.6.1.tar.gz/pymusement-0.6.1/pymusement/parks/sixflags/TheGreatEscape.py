from pymusement.parks.sixflags.SixFlagsPark import SixFlagsPark
    
class TheGreatEscape(SixFlagsPark):
    def __init__(self):
        super(TheGreatEscape, self).__init__()

    def getId(self):
        return 24
    def getCity(self):
        return 'Queensbury'
    def getName(self):
        return 'The Great Escape'

    