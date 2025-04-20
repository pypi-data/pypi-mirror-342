import unittest
from nose.tools import *

from pymusement.park import Park
from pymusement.show import Show
from pymusement.ride import Ride

class ParkTestCase(unittest.TestCase):
    @raises(Exception)
    def test_rides_no_rides(self):
        park = Park()
        self.assertEqual(park.rides(), [])

    @raises(Exception)
    def test_shows_no_shows(self):
        park = Park()
        self.assertEqual(park.shows(), [])

    def test_addRide(self):
        park = Park()
        ride = Ride()
        park.addRide(ride)
        self.assertEqual(len(park.rides()), 1)

    def test_addShow(self):
        park = Park()
        show = Show()
        park.addShow(show)
        self.assertEqual(len(park.shows()), 1)
