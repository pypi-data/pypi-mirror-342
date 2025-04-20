from pymusement.attraction import Attraction
class Ride(Attraction):

    _added_keys = ['wait', 'isOpen', 'status', 'single_rider', 'skipLine']

    def __init__(self):
        super(Ride, self).__init__()
        self._addKeys(self._added_keys)

    def setOpen(self):
        self['isOpen'] = True

    def setClosed(self):
        self['isOpen'] = False
    def setStatus(self, status):
        self['status'] = status
    def setTime(self, time):
        if(isinstance(time, str)):
            time = int(time)
        self['wait'] = time

    def setSingleRider(self, time):
        if(isinstance(time, str)):
            time = int(time)
        self['single_rider'] = time
    
    def has_skip_line(self):
        if self['skipLine'] == True:
            return True
        else:
            return False
        
    def set_skip_line(self, status):
        self['skipLine'] = status
    
    def isOpen(self):
        if self['isOpen'] == True:
            return True
        else:
            return False
