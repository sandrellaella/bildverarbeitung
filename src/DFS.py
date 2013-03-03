# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:09:30 2013

@author: sandra
"""

class Node:
    #Initialisierung der Knoten
    #Vorgaenger = NIL
    #Besucht = FALSE
    #Jeder Knoten erhaelt eine Nummer
    def __init__(self,features,i):
        self.nodenumber = i
        self.visited = False
        self.feature = features[i]
        self.predecessor = "nil"
        
    def getPredecessor(self):
        return self.predecessor

    def setPredecessor(self,predecessor):
        self.predecessor = predecessor
        
    def setVisited(self):
        self.visited = True
        
    def getVisitedState(self):
        return self.visited
        
    def getFeaturePoint(self):
        return self.feature
        

def findNeighbours(node,nodes,searchDistance):
    neighbours = []
    current = node.feature
    x = current[0]
    y = current[1]
    for n in nodes:
        if n.visited is False:
            x1 = n.feature[0]
            y1 = n.feature[1]
            if x1>=x-searchDistance and x1<=x or x1<=x+searchDistance and x1>=x:
                if y1>=y-searchDistance and y1<=y or y1<=y+searchDistance and y1>=y:        
                    neighbours.append((x1,y1))
    return neighbours

def DFSVisit(node):
    node.setVisited()
    neighbours = findNeighbours(node,nodes,30)
    #print node.nodenumber, " : ", neighbours
    for neighbour in neighbours:
        print neighbour
        if neighbour.visited is False:
            neighbour.predecessor = node
            DFSVisit(neighbour)
    


def DFS(nodes):
    for i in range(len(nodes)):
        if nodes[i].visited == False:
            DFSVisit(nodes[i])
            

    


features = [(183.0, 225.0), (174.0, 177.0), (206.0, 245.0), (205.0, 185.0), (220.0, 176.0), (25.0, 224.0), (187.0, 191.0), (191.0, 170.0), (196.0, 235.0), (176.0, 160.0), (155.0, 168.0), (266.0, 128.0), (143.0, 25.0), (83.0, 49.0), (203.0, 71.0), (156.0, 93.0), (145.0, 44.0), (150.0, 68.0), (160.0, 109.0), (168.0, 132.0), (203.0, 133.0), (185.0, 213.0), (43.0, 227.0), (99.0, 250.0), (105.0, 97.0), (91.0, 69.0), (53.0, 231.0), (146.0, 250.0), (86.0, 245.0), (164.0, 122.0), (63.0, 235.0), (153.0, 81.0), (160.0, 243.0), (172.0, 149.0), (196.0, 154.0), (200.0, 144.0), (148.0, 58.0), (203.0, 116.0), (203.0, 94.0), (117.0, 252.0), (186.0, 201.0), (203.0, 106.0), (100.0, 87.0), (232.0, 170.0), (248.0, 154.0), (257.0, 142.0), (123.0, 132.0), (134.0, 150.0), (169.0, 235.0), (140.0, 158.0)]
count = len(features)

nodes = []

#Zuordnung Features zu Knoten 
for i in range(count):
    nodes.append(Node(features,i))

    
DFS(nodes)
    


