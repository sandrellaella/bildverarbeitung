# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:09:30 2013

@author: sandra
"""

import cv

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
        self.postdecessor = "nil"
        self.whichpath = "nil"
        self.distance = 0
        
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

#Finde den nächsten Knoten, der auch keinen Nachfolger hat. Diser
#Knoten darf aber nicht auf dem gleichen Pfad sein.        
def findNextFeature(node,remainingNodes):
    feature_of_node = node.feature
    distance_min = 1000
    distances = []
    distance = 0
    node_candidate = ""
    for n in remainingNodes:
        if n is not node:
            distance = ((feature_of_node[0]-n.feature[0])**2 + (feature_of_node[1]-n.feature[1])**2)**0.5
            distances.append((n,distance)) 
            #print node.feature, distances
        for d in distances:
            node_d = d[0]
            node_dist = d[1]
            if node_dist < distance_min:
                distance_min = node_dist
                node_candidate = node_d
                n.distance = distance_min
                
            
        
    return (distance_min,node_candidate)
        
def getPath(goal,pathnumber):
    path_stack = []
    path_stack.append(goal)
    goal.whichpath = pathnumber
    while goal.predecessor is not "nil":
        goal = goal.predecessor 
        path_stack.append(goal)
    return path_stack
        

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
                    neighbours.append(n)
                
    return neighbours

def DFSVisit(node,nodes,searchDistance):
    node.setVisited()
    neighbours = findNeighbours(node,nodes,searchDistance)
    for neighbour in neighbours:
        if neighbour.visited is False:
            neighbour.predecessor = node
            node.postdecessor = neighbour
            DFSVisit(neighbour,nodes,searchDistance)     

def DFS(nodes,searchDistance):
    for i in range(len(nodes)):
        if nodes[i].visited == False:
            DFSVisit(nodes[i],nodes,searchDistance)
    return nodes
            

features = [(183.0, 225.0), (174.0, 177.0), (206.0, 245.0), (205.0, 185.0), (220.0, 176.0), (25.0, 224.0), (187.0, 191.0), (191.0, 170.0), (196.0, 235.0), (176.0, 160.0), (155.0, 168.0), (266.0, 128.0), (143.0, 25.0), (83.0, 49.0), (203.0, 71.0), (156.0, 93.0), (145.0, 44.0), (150.0, 68.0), (160.0, 109.0), (168.0, 132.0), (203.0, 133.0), (185.0, 213.0), (43.0, 227.0), (99.0, 250.0), (105.0, 97.0), (91.0, 69.0), (53.0, 231.0), (146.0, 250.0), (86.0, 245.0), (164.0, 122.0), (63.0, 235.0), (153.0, 81.0), (160.0, 243.0), (172.0, 149.0), (196.0, 154.0), (200.0, 144.0), (148.0, 58.0), (203.0, 116.0), (203.0, 94.0), (117.0, 252.0), (186.0, 201.0), (203.0, 106.0), (100.0, 87.0), (232.0, 170.0), (248.0, 154.0), (257.0, 142.0), (123.0, 132.0), (134.0, 150.0), (169.0, 235.0), (140.0, 158.0)]
count = len(features)
img = cv.LoadImage("hand.jpg")
nodes = []
searchDistance = 20

#Zuordnung Features zu Knoten 
for i in range(count):
    nodes.append(Node(features,i))
    
nodes = DFS(nodes,searchDistance)

path_list = []
pathnumber = 1
for i in range(len(nodes)):
    path = getPath(nodes[i],pathnumber)
    path_list.append((path,pathnumber))
    pathnumber = pathnumber + 1


remainingNodes = []
#Pfade zeichnen und Knoten einzeichnen, die keinen Nachfolger haben   
color = 255
for path in path_list:
    for p in path[0]:
        x1 = int(p.feature[0])
        y1 = int(p.feature[1])
        if p.predecessor is not "nil":
            x2 = int(p.predecessor.feature[0])
            y2 = int(p.predecessor.feature[1])
            cv.Line(img, (x1,y1),(x2,y2), (color,color,color), thickness=2, lineType=8, shift=0)
        if p.postdecessor is "nil":
            #cv.Circle(img,(int(p.feature[0]),int(p.feature[1])),5,(255,0,255),thickness=2)
            remainingNodes.append(p)

#print path_list
#Naechsten Nachbar finden, der keinen Nachfolger hat. 
color = 50
color2 = 10
for node in remainingNodes:
    print node.distance
    best_distance_candidate = findNextFeature(node,remainingNodes)
    #print best_distance_candidate
    candidate = best_distance_candidate[1]
    print candidate.distance
    if candidate.predecessor is not "nil":
        cv.Line(img, (int(node.feature[0]),int(node.feature[1])),(int(candidate.feature[0]),int(candidate.feature[1])), (color,color,255), thickness=2, lineType=8, shift=0)
cv.ShowImage("Image",img)
cv.WaitKey()
