"""Finde den naechstgelegenen Knoten aus einer Knoten-Liste von dem Knoten
node aus."""
def findNextFeature(node,nodeList):
    distance_min = 10000
    distances = []
    distance = 0
    node_candidate = ""
    for n in nodeList:
        if n is not node:
            #euklidischer Abstand
            distance = ((node.feature[0]-n.feature[0])**2 + (node.feature[1]-n.feature[1])**2)**0.5
            distances.append((n,distance))
        #Welcher Knoten hat den minimalen Abstand zu Knoten d?
        for d in distances:
            node_d = d[0]
            node_dist = d[1]
            if node_dist < distance_min:
                distance_min = node_dist
                node_candidate = node_d
                n.distance = distance_min
    return (distance_min,node_candidate)