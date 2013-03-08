"""Tiefensuche. Der Aufruf der Tiefensuche erfolgt ueber die Funktion
DFS(nodes,searchDistance). Wenn ein Knoten gefunden wurde, der noch 
nicht besucht wurde, wird ein neuer Baum erzeugt. Der Knoten bildet
dann die Wurzel des Baumes. Der Baum ist eine Zusammenhangskomponente."""

# Teil der Tiefensuche. Ein Baum. 
def DFSVisit(node,nodes,searchDistance,Component_number):
    node.setVisited()
    node.setComponent(Component_number)
    #FindNeighbours wie in der Breitensuche (Suchkreuz)
    neighbours = findNeighbours(node,nodes,searchDistance)
    for neighbour in neighbours:
        if neighbour.visited is False:
            neighbour.predecessor = node
            node.postdecessor = neighbour
            DFSVisit(neighbour,nodes,searchDistance,Component_number)     

# Tiefensuche Startup.
def DFS(nodes,searchDistance):
    component = 0
    for i in range(len(nodes)):
        if nodes[i].visited == False:
            DFSVisit(nodes[i],nodes,searchDistance,component)
            #Wenn keine Knoten mehr gefunden werden koennen, wird
            #nach einem weiteren Knoten gesucht, der noch nicht
            #besucht wurde (solange es noch
            #unbesuchte Knoten gibt). Diese Komponente ist jetzt fertig.
            #Neue Komponente anfangen.
            component = component + 1
    return nodes