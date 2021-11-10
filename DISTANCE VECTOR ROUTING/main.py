import sys
import subprocess
import platform
from Node import Node

allNodeIds = [] 
def _main( fileName ) :
    topology = {} 
    with open( fileName, 'r' ) as fp :
        lines = fp.read().replace('\r', '' ).split( '\n' )
        for line in lines:
            if ( line == '' ) : 
                continue
            from_, to_, cost = line.split()
            if from_ not in topology:
                topology[from_] = [ (to_, cost) ]
            else:
                topology[from_].append( (to_,cost) )

            if to_ not in topology:
                topology[to_] = [ (from_, cost) ]
            else:
                topology[to_].append( (from_,cost) )
    for node_id, neighbors in topology.items():
        if node_id not in allNodeIds:
            allNodeIds.append(node_id)
        newNode = Node(node_id, neighbors) 

    allNodeIds.sort()
    print(topology)
    for node_id in allNodeIds:
        node = Node.findNode(node_id)
        node.initializeDistanceTable()
        node.initializeRoutingTable()

    print("\nThis program will simulate the Distance-Vector Routing Protocol.\n")
    while True:
        modeSelect = input("Press 1 to show the iterations\n")
        if modeSelect == '1':
            autoMode()
            break
        else: 
            print("Error: Enter 1 to show the iterations")

def autoMode():
    print("\nPerforming iterations")
    loopCount = 1
    curr_state = 'default' 
    last_state = 'default' 

    while True:
        curr_node = '1'
        node = Node.findNode( curr_node )
        node.updateDistanceTable()

        curr_state = ''
        for node_id in allNodeIds:
            node = Node.findNode(node_id)
            curr_state += node.displayTables()
            curr_state += '\n'
        if curr_state != last_state:
            last_state = curr_state
            loopCount +=1
        else: 
            break
    print("===================================")
    print(f"Stable State Reached after {loopCount} iterations.")
    print("===================================")

    stable_state = ''
    for node_id in allNodeIds:
        node = Node.findNode(node_id)
        stable_state += node.displayTables()
        stable_state += '\n'
    print(stable_state) 

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

if __name__ == '__main__' :
  if len( sys.argv ) != 2 : 
    raise ValueError( 'Include input file name in command line arguments.' )
  _main( sys.argv[1] )
