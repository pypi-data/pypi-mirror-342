from pymusement.parks.universal.UniversalPark import UniversalPark

class UniversalEpicUniverse(UniversalPark):
    def __init__(self):
        super(UniversalEpicUniverse, self).__init__()

    def getId(self):
        return 24000
    def getCity(self):
        return 'Orlando'
    def getName(self):
        return 'Universal Epic Universe'
