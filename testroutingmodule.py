#
# CSCI 4760 -- unit test for link-state router
# Template provided by Dr Dan, completed by student
# 
import unittest
from routingmodule import RoutingModule
from linkstatemsg import LinkStateMsg



class TestRoutingModule(unittest.TestCase):
    """
    Class that tests the constructor, receive_message, distance, is_reachable, and
    first_hop methods from the RoutingModule class
    """

    def test_setup(self):
        """
        Tests the reachability, distance to the original node created
        Tests reachability to not yet created nodes
        :return:
        """
        router = RoutingModule("A")
        self.assertTrue(router.is_reachable("A"))
        self.assertTrue(router.distance("A") == 0)
        self.assertFalse(router.is_reachable("B"))
        self.assertFalse(router.is_reachable("C"))

    def test_buildgraph(self):
        """
        Tests each of the functions on a fully created graph. Puts links up
        and takes several of them down to check how routes differ after links
        go down
        :return:
        """
        # Creates new routing module
        router = RoutingModule("A")
        #Fully fills the graph
        router.receive_message(LinkStateMsg("A","B",3.2,"up"))
        router.receive_message(LinkStateMsg("B","C",0.8,"up"))
        router.receive_message(LinkStateMsg("E","D",4.1,"up"))
        router.receive_message(LinkStateMsg("B","E",1.5,"up"))
        router.receive_message(LinkStateMsg("E","F",1.4,"up"))
        router.receive_message(LinkStateMsg("C","F",7.7,"up"))
        router.receive_message(LinkStateMsg("F","G",3.2,"up"))

        #verify the distance, reachability, and first_hop of all nodes
        self.assertTrue(router.distance("A") == 0)
        self.assertTrue(router.is_reachable("A"))
        self.assertTrue(router.first_hop("A") == "A")

        self.assertTrue(router.distance("B") == 3.2)
        self.assertTrue(router.is_reachable("B"))
        self.assertTrue(router.first_hop("B") == "B")

        self.assertTrue(router.distance("C") == 4.0)
        self.assertTrue(router.is_reachable("C"))
        self.assertTrue(router.first_hop("C") == "B")

        self.assertTrue(router.distance("D") == 8.8)
        self.assertTrue(router.is_reachable("D"))
        self.assertTrue(router.first_hop("D") == "B")

        self.assertTrue(router.distance("E") == 4.7)
        self.assertTrue(router.is_reachable("E"))
        self.assertTrue(router.first_hop("E") == "B")

        self.assertTrue(router.distance("F") == 6.1)
        self.assertTrue(router.is_reachable("F"))
        self.assertTrue(router.first_hop("F") == "B")

        self.assertTrue(router.distance("G") == 9.3)
        self.assertTrue(router.is_reachable("G"))
        self.assertTrue(router.first_hop("G") == "B")

        # Make the link from B to C go down
        router.receive_message(LinkStateMsg("B","C",0.8,"down"))

        #verify the distance, reachability, and first_hop of all nodes after taking
        #Link from B to C down
        self.assertTrue(router.distance("A") == 0)
        self.assertTrue(router.is_reachable("A"))
        self.assertTrue(router.first_hop("A") == "A")

        self.assertTrue(router.distance("B") == 3.2)
        self.assertTrue(router.is_reachable("B"))
        self.assertTrue(router.first_hop("B") == "B")

        self.assertTrue(router.distance("C") == 13.8)
        self.assertTrue(router.is_reachable("C"))
        self.assertTrue(router.first_hop("C") == "B")

        self.assertTrue(router.distance("D") == 8.8)
        self.assertTrue(router.is_reachable("D"))
        self.assertTrue(router.first_hop("D") == "B")

        self.assertTrue(router.distance("E") == 4.7)
        self.assertTrue(router.is_reachable("E"))
        self.assertTrue(router.first_hop("E") == "B")

        self.assertTrue(router.distance("F") == 6.1)
        self.assertTrue(router.is_reachable("F"))
        self.assertTrue(router.first_hop("F") == "B")

        self.assertTrue(router.distance("G") == 9.3)
        self.assertTrue(router.is_reachable("G"))
        self.assertTrue(router.first_hop("G") == "B")

        # Takes links from C to F and E to F down
        router.receive_message(LinkStateMsg("C","F",7.7,"down"))
        router.receive_message(LinkStateMsg("E","F",1.4,"down"))


        #verify the distance, reachability, and first_hop of all nodes after taking
        #Link from C to F down and E to F down
        self.assertTrue(router.distance("A") == 0)
        self.assertTrue(router.is_reachable("A"))
        self.assertTrue(router.first_hop("A") == "A")

        self.assertTrue(router.distance("B") == 3.2)
        self.assertTrue(router.is_reachable("B"))
        self.assertTrue(router.first_hop("B") == "B")

        self.assertTrue(router.distance("C") == -1)
        self.assertFalse(router.is_reachable("C"))
        self.assertTrue(router.first_hop("C") == None)

        self.assertTrue(router.distance("D") == 8.8)
        self.assertTrue(router.is_reachable("D"))
        self.assertTrue(router.first_hop("D") == "B")

        self.assertTrue(router.distance("E") == 4.7)
        self.assertTrue(router.is_reachable("E"))
        self.assertTrue(router.first_hop("E") == "B")

        self.assertTrue(router.distance("F") == -1)
        self.assertFalse(router.is_reachable("F"))
        self.assertTrue(router.first_hop("F") == None)

        self.assertTrue(router.distance("G") == -1)
        self.assertFalse(router.is_reachable("G"))
        self.assertTrue(router.first_hop("G") == None)

        # Puts all links that went down back up
        router.receive_message(LinkStateMsg("B","C",0.8,"up"))
        router.receive_message(LinkStateMsg("C","F",7.7,"up"))
        router.receive_message(LinkStateMsg("E","F",1.4,"up"))

        # Verifies after putting links back up
        # Should equal what they did in the first test
        self.assertTrue(router.distance("A") == 0)
        self.assertTrue(router.is_reachable("A"))
        self.assertTrue(router.first_hop("A") == "A")

        self.assertTrue(router.distance("B") == 3.2)
        self.assertTrue(router.is_reachable("B"))
        self.assertTrue(router.first_hop("B") == "B")

        self.assertTrue(router.distance("C") == 4.0)
        self.assertTrue(router.is_reachable("C"))
        self.assertTrue(router.first_hop("C") == "B")

        self.assertTrue(router.distance("D") == 8.8)
        self.assertTrue(router.is_reachable("D"))
        self.assertTrue(router.first_hop("D") == "B")

        self.assertTrue(router.distance("E") == 4.7)
        self.assertTrue(router.is_reachable("E"))
        self.assertTrue(router.first_hop("E") == "B")

        self.assertTrue(router.distance("F") == 6.1)
        self.assertTrue(router.is_reachable("F"))
        self.assertTrue(router.first_hop("F") == "B")

        self.assertTrue(router.distance("G") == 9.3)
        self.assertTrue(router.is_reachable("G"))
        self.assertTrue(router.first_hop("G") == "B")


if __name__ == '__main__':
	unittest.main()

