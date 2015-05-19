import unittest
from linkstatemsg import LinkStateMsg


class TestLinkStateMsgClass(unittest.TestCase):
    """
    Tests LinkStateMsg class that represents source,
    destination, metric, and state of a link
    """

    def test_constructor(self):
        mylinkstate = LinkStateMsg("source", "destination", 7, "up")
        self.assertTrue(mylinkstate.source == "source")
        self.assertTrue(mylinkstate.destination == "destination")
        self.assertTrue(mylinkstate.metric == 7)
        self.assertTrue(mylinkstate.linkState == "up")


if __name__ == '__main__':
    unittest.main()
