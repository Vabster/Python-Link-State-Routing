import unittest
from route import route

class TestRouteClass(unittest.TestCase):
    """
      Test of entity class Route, which represents a
	     routing table entry
    """
    def test_constructor(self): 
	    myroute = route("San Francisco","Atlanta",2536)
	    self.assertTrue(myroute.distance == 2536)
	    self.assertTrue(myroute.destination == "San Francisco")
	    self.assertTrue(myroute.firsthop == "Atlanta")

if __name__ == '__main__':
	unittest.main()

