class Node():
    class_All_Nodes = {}   
    @classmethod
    def addNode( cls, a_node ) :
        node_id = a_node.id
        if node_id in cls.class_All_Nodes :
            raise ValueError( f'Redeclaration of Node {node_id!r}.' )
        cls.class_All_Nodes[ node_id ] = a_node

    @classmethod
    def findNode( cls, node_id ) :
        return cls.class_All_Nodes.get( node_id, None )

    @classmethod
    def updateLink(cls, node_1_id, node_2_id, distance):
        node1 = cls.findNode(node_1_id)
        node2 = cls.findNode(node_2_id)

        node1.distanceTable[node_2_id] = distance
        node2.distanceTable[node_1_id] = distance
        print("-----------------------------------")
        print(f"Link between Node {node_1_id} and Node {node_2_id} updated. New link cost = {distance}.")
        print("-----------------------------------")

    def __init__(self, node_id, neighbors = []):
        self.id = node_id
        self.neighbors = neighbors 
        self.distanceTable = {} 
        self.routingTable = {} 

        for neighbor, cost in neighbors:
            self.distanceTable[neighbor] = cost
        Node.addNode(self) 
    def initializeDistanceTable(self):
        for node_id in Node.class_All_Nodes:
            if node_id not in self.distanceTable:
                self.distanceTable[node_id] = 16
            self.distanceTable[ self.id ] = 0
    def initializeRoutingTable(self):
        for node_id in Node.class_All_Nodes:
            if self.isNeighbor(node_id):
                self.routingTable[node_id] = node_id
            elif node_id == self.id:
                self.routingTable[node_id] = self.id
            else:
                self.routingTable[node_id], _ = self.neighbors[0]
    def displayTables(self):
        res = ""
        res += f"Node {self.id}\n"
        res += "-----------------------------------\n"
        for node_id in sorted(self.distanceTable):
            res += f"Destination Node: {node_id}     Shortest Distance: {self.distanceTable[node_id]}    Route to Node: {self.routingTable[node_id]}\n"
        res += "-----------------------------------"
        return res

    def isNeighbor(self, a_node_id):
        for neighbor_id, cost in self.neighbors:
            if a_node_id == neighbor_id:
                return True
        return False
    def updateDistanceTable(self):
        for node_id, distance in self.distanceTable.items():
            if node_id == self.id:
                continue
            originalDistance = self.distanceTable[node_id]

            for neighbor_id, cost in self.neighbors:
                neighbor = Node.findNode(neighbor_id)
                if int( self.distanceTable[node_id] ) > int( neighbor.distanceTable[node_id] ) + int(cost):
                    self.distanceTable[node_id] = str( int( neighbor.distanceTable[node_id] ) + int(cost) )
                    self.routingTable[node_id] = neighbor_id
                    neighbor.updateDistanceTable()
