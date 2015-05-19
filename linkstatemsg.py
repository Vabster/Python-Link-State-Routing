"""
Class that represents a Link State Message
"""
class LinkStateMsg:
    """
    Constructor that sets the values of the source,
    destination, link metric, and a state message ("up" or "down")
    """
    def __init__(self, source, destination, metric, linkState):
        self.source = source
        self.destination = destination
        self.metric = metric
        self.linkState = linkState
