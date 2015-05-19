from linkstatemsg import LinkStateMsg
from route import route
"""
Class that represents the actual Link-State routing engine
"""
class RoutingModule:
    """
    Constructor that creates initally empty
    routing table and link-state message cache
    """
    def __init__(self, node):
        self.originalNode = node            # Sets the original node created in the constructor
        self.nodes = [node]                 # Creates a list of nodes in the graph
        self.distances = {                  # Has a dictionary of the distances from all nodes to directly linked neighbors
        node:{}
        }
        self.firstHopper = [[self.originalNode, self.originalNode, 0]]      # Keeps track of firstHop distances to each node
        self.routeStats = [
                                [node, node, 0, node]
                            ] # List of lists of routes from nodes to all other nodes [source, destination, distance, firsthop]
        self.LinkStateMessages = [
                                    [node, node, 0, "up"]
                                ] # List of lists that store the current LinkState Messages
        self.visited = {self.originalNode: 0}       # List of all visited nodes and sitances to them

    def is_reachable(self, destination):
        """
        Checks if node is reachable if so, returns True, if not returns false
        """
        if self.visited.has_key(destination):
            return True
        else:
            return False

    def distance(self, destination):
        """
        Checks distance to a node, if reachable, returns the distance, if not returns -1
        """
        if self.visited.has_key(destination):
            return self.visited[destination]
        else:
            return -1

    def first_hop(self, destination):
        """
        Returns first hop to a particular node, if it is not reachable then it returns None
        """
        for route in self.firstHopper:
            if route[0] == destination:
                return route[1]
        return None
    def outgoing_links(self, node):
        if self.distances.has_key(node):
            return len(self.distances[node].keys())
        else:
            return None

    def receive_message(self, msg):
        """
        Updates lists created in constructor
        First checks for LinkStateMessage received and checks if it already exists
        in the LinkStateMessages list. If it does not it will run dijkstra's algorithm
        and update all the other lists/dictionaries and compute the distances to them.
        """
        for message in self.LinkStateMessages:
            """
            Goes through LinkStateMessages and checks if the msg already exists.
            If it does it returns because there would be no reason to update the
            lists/dictionaries. If not it adds msg to list
            """
            if message[0] == msg.source and message[1] == msg.destination:
                if message[2] == msg.metric and  message[3] == msg.linkState:
                    return
                message[2] = msg.metric
                message[3] = msg.linkState
                break
        else:
            self.LinkStateMessages.append([msg.source,msg.destination,msg.metric,msg.linkState])

        # Checks if msg.source is in dictionary. Updates dictionary if so.
        # If not, it adds the key and then updates the dictionary.
        if self.distances.has_key(msg.source):
            # Checks if the link state is "down", if so it removes
            # the link from the distances dictionary
            if msg.linkState == "down":
                if self.distances[msg.source].has_key(msg.destination):
                    del self.distances[msg.source][msg.destination]
            else:
                self.distances[msg.source][msg.destination] = msg.metric
        else:
            # Checks if the link state is "down", if so it removes
            # the link from the distances dictionary. If not it adds
            # it to the dictionary
            if msg.linkState == "down":
                self.distances[msg.source] = {}
                #self.distances[msg.source][msg.source] = 0
                self.nodes.append(msg.source)
            else:
                # Adds newly added node to our nodes list
                self.nodes.append(msg.source)
                self.distances[msg.source] = {}
                #self.distances[msg.source][msg.source] = 0
                self.distances[msg.source][msg.destination] = msg.metric
        # Checks if msg.destination is in dictionary. Updates dictionary if so.
        # If not, it adds the key and then updates the dictionary.
        if self.distances.has_key(msg.destination):
            # Checks if the link state is "down", if so it removes
            # the link from the distances dictionary. If not it adds
            # it to the dictionary
            if msg.linkState == "down":
                if self.distances[msg.destination].has_key(msg.source):
                    del self.distances[msg.destination][msg.source]
            else:
                self.distances[msg.destination][msg.source] = msg.metric
        else:
            # Checks if the link state is "down", if so it removes
            # the link from the distances dictionary. If not it adds
            # it to the dictionary
            if msg.linkState == "down":
                self.nodes.append(msg.destination)
                self.distances[msg.destination] = {}
                #self.distances[msg.destination][msg.destination] = 0
            else:
                # Adds newly added node to our nodes list
                self.nodes.append(msg.destination)
                self.distances[msg.destination] = {}
                #self.distances[msg.destination][msg.destination] = 0
                self.distances[msg.destination][msg.source] = msg.metric

        # Initializes values used to compute dijkstra's algorithm

        currentNode = self.originalNode
        linkedDistance = 0
        self.visited = {}
        iteration = 0
        notChecked = {}
        for node in self.nodes:
            # Adds node to notChecked list
            notChecked[node] = None
        notChecked[currentNode] = linkedDistance
        self.firstHopper = [[self.originalNode, self.originalNode, 0]]
        firstHopList = []
        currentFirstHop = ""
        while True:
            """
            Computes distance to a neighbor and determines if it is
            the shortest distance reached thus far
            """
            for directlyLinked, distance in self.distances[currentNode].items():
                """
                Updates firsthopList and currentFirstHop based on neighbor
                """
                if currentNode == self.originalNode:
                    firstHopList.append(directlyLinked)
                    currentFirstHop = directlyLinked
                elif currentNode in firstHopList:
                    currentFirstHop = currentNode

                # Continues if all linked nodes have been checked
                if directlyLinked not in notChecked:
                    continue

                # Updates distance and nodes to be checked/used
                newDistance = linkedDistance + distance
                if notChecked[directlyLinked] is None or notChecked[directlyLinked] > newDistance:
                    index = 0
                    for row in self.firstHopper:
                        if row[0] == directlyLinked:
                            row = [directlyLinked,currentFirstHop, newDistance]
                            self.firstHopper[index] = row
                            break
                        index = index + 1
                    else:
                        self.firstHopper.append([directlyLinked,currentFirstHop, newDistance])
                    notChecked[directlyLinked] = newDistance
            self.visited[currentNode] = linkedDistance
            del notChecked[currentNode]
            if not notChecked:
                break
            nearbyNodes = [node for node in notChecked.items() if node[1]]
            if len(nearbyNodes) > 0:
                currentNode, linkedDistance = sorted(nearbyNodes, key = lambda x: x[1])[0]
            else:
                break

