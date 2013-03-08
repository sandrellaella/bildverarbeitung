# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:09:30 2013

@author: sandra

Idee: Alle Komponenten mit Komponente 0 verbinden.
Ansatz: Jede Komponente (ausser die erste) einzelnd durchgehen und die Kuerzeste Verbindung 
	  zwischen einem offenen Ende der Komponente und einem offenen Ende einer anderen Komponente
	  suchen. Dann die Komponenten vereinen. Nachdem alle Komponenten bearbeitet wurden ist sind
	  alle Komponenten miteinander verbunden. -> Pixelkonnektivitaet
"""

import cv

class Node:
    #Initialisierung der Knoten
    #Jeder Knoten erhaelt eine Nummer
    def __init__(self,features,i):
        self.nodenumber = i
        self.visited = False
        self.feature = features[i]
        self.predecessor = "nil"
        self.postdecessor = "nil"
        self.whichpath = "nil"
        self.distance = 0
        self.component = "nil"
        
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

    def setComponent(self, Component_number):
        self.component = Component_number

    def getComponent(self):
        return self.component


def getPath(goal,pathnumber):
    path_stack = []
    path_stack.append(goal)
    goal.whichpath = pathnumber
    while goal.predecessor is not "nil":
        goal = goal.predecessor 
        path_stack.append(goal)
    return path_stack
    

#Finde den naechstgelegenen Knoten aus einer Knoten-Liste.
def findNextFeature(node,nodeList):
    distance_min = 10000
    distances = []
    distance = 0
    node_candidate = ""
    for n in nodeList:
        if n is not node:
            distance = ((node.feature[0]-n.feature[0])**2 + (node.feature[1]-n.feature[1])**2)**0.5
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

# Teil der Tiefensuche. Ein Baum. 
def DFSVisit(node,nodes,searchDistance,Component_number):
    node.setVisited()
    node.setComponent(Component_number)
    neighbours = findNeighbours(node,nodes,searchDistance)
    for neighbour in neighbours:
        if neighbour.visited is False:
            neighbour.predecessor = node
            node.postdecessor = neighbour
            DFSVisit(neighbour,nodes,searchDistance,Component_number)     

# Tiefensuche
def DFS(nodes,searchDistance):
    component = 0
    for i in range(len(nodes)):
        if nodes[i].visited == False:
            DFSVisit(nodes[i],nodes,searchDistance,component)
            component = component + 1
    return nodes
            
def GetOpenEnds(nodelist):
    openends = []
    for node in nodelist:     
        if node.predecessor == "nil" or node.postdecessor == "nil":
            openends.append(node)
    return openends

def GetNodesWithNotComponent(nodelist,NotComponent):
    NodesNotComponent = []
    for node in nodelist:
        if node.component != NotComponent:
            NodesNotComponent.append(node)
    return NodesNotComponent

def GetNodesWithComponent(nodelist,NotComponent):
    NodesNotComponent = []
    for node in nodelist:
        if node.component == NotComponent:
            NodesNotComponent.append(node)
    return NodesNotComponent

def CalcNotConnected(nodelist,ComponentNumber):
    Components = []
    for n in nodelist:
            Components.append(n.component)
    #print Components
    NumNotConnected = len(Components)-Components.count(ComponentNumber)
    return NumNotConnected

def NumComponents(nodelist):
    Num = 0
    components = []
    for n in nodelist:
        if components.count(n.component) == 0:
            Num = n.component+1
            components.append(n.component)
    return Num

def drawDFSPath(nodes,img):
  path_list = []
  pathnumber = 1
  for i in range(len(nodes)):
    path = getPath(nodes[i],pathnumber)
    path_list.append((path,pathnumber))
    
    color = 255
    for path in path_list:
      for p in path[0]:
        x1 = int(p.feature[0])
        y1 = int(p.feature[1])
        if p.predecessor is not "nil":
            x2 = int(p.predecessor.feature[0])
            y2 = int(p.predecessor.feature[1])
            cv.Line(img, (x1,y1),(x2,y2), (color,color,color), thickness=2, lineType=8, shift=0)

#Features features und Bild img muessen vom Benutzer selbst gesetzt werden.

#######BEGINN: Erste Verarbeitungsstufe. Ausfuehren der Tiefensuche.####### 
#Zuordnung Features zu Knoten 
nodes = []
for i in range(len(features)):
    nodes.append(Node(features,i))
#DFS ausfuehren    
nodes = DFS(nodes,searchDistance)
#Pfad zeichnen
drawDFSPath(nodes,img)

#######ENDE: Erste Verarbeitungsstufe#######

#######BEGINN: Zweite Verarbeitungsstufe. Verbinden der Zusammenhangskomponenten#######
OpenEnds = []
OpenEnds = GetOpenEnds(nodes)
NumComps = NumComponents(OpenEnds)
  
#Jede Komponente nacheinander durchgehen
for i in range(NumComps): 
     #Komponente 0 ist Referenz-Komponente.
     if i > 0: 
       #Offene Enden aus der zur Zeit betrachteten Komponente i
       OpenEndsInComponentToConnect = GetNodesWithComponent(OpenEnds,i)
       #Moegliche Verbindungsknoten zu anderen Komponenten (Knoten aus OpenEnds).
       OpenEndsInOtherComponents = GetNodesWithNotComponent(OpenEnds,i)
       #Kuerzeste Verbindung zu einer anderen Komponente
       bestlink = (0,"nil")
       #Knoten der aktuellen Komponente, mit dem die Verbindung eingegangen wird.
       ConnectNode = "nil" 
       # Alle Kandidaten durchgehen und die beste Verbindung waehlen.
       for n in OpenEndsInComponentToConnect: 
         #Kuerzeste Verbindung vom aktuellen Knoten zu einer anderen Komponente
         PossibleLink = findNextFeature(n,OpenEndsInOtherComponents) 
         #Verbindung ist kurzer als alle zuvor vorgeschlagenen
         if bestlink[1] is "nil" or bestlink[0]>PossibleLink[0]: 
           bestlink = PossibleLink                  
           ConnectNode = n
         cv.Line(img, (int(ConnectNode.feature[0]),int(ConnectNode.feature[1])),(int(bestlink[1].feature[0]),int(bestlink[1].feature[1])), (0,255,0), thickness=2, lineType=8, shift=0)
         print "-------->  Damit ist Komponente", ConnectNode.component, " mit Komponente ", bestlink[1].component, " verbunden."
        #Update der Komponente fuer die OpenEnds der aktuellen Komponente
         for n in OpenEndsInComponentToConnect:
           n.setComponent(bestlink[1].component)
        
        
#######ENDE: Zweite Verarbeitungsstufe#######


#######BEGINN: Ueberpruefen der Konnektivitaet#######

for n in OpenEnds:
    ComponentNodes = GetNodesWithComponent(nodes, n.component)
    for m in ComponentNodes:
        m.setComponent(n.component)
ComponentNodes = GetNodesWithComponent(nodes, 0)
components = []
for n in ComponentNodes:
    components.append(n.component)
if len(components)==components.count(0):
    print "Pixelkonnektivitaet ist gegeben! :-) :-) :-)"

#######ENDE: Ueberpruefen der Konnektivitaet#######