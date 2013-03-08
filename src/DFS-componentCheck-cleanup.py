# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:09:30 2013

@author: sandra
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

  
#Hand-Features
features = [(183.0, 225.0), (174.0, 177.0), (206.0, 245.0), (205.0, 185.0), (220.0, 176.0), (25.0, 224.0), (187.0, 191.0), (191.0, 170.0), (196.0, 235.0), (176.0, 160.0), (155.0, 168.0), (266.0, 128.0), (143.0, 25.0), (83.0, 49.0), (203.0, 71.0), (156.0, 93.0), (145.0, 44.0), (150.0, 68.0), (160.0, 109.0), (168.0, 132.0), (203.0, 133.0), (185.0, 213.0), (43.0, 227.0), (99.0, 250.0), (105.0, 97.0), (91.0, 69.0), (53.0, 231.0), (146.0, 250.0), (86.0, 245.0), (164.0, 122.0), (63.0, 235.0), (153.0, 81.0), (160.0, 243.0), (172.0, 149.0), (196.0, 154.0), (200.0, 144.0), (148.0, 58.0), (203.0, 116.0), (203.0, 94.0), (117.0, 252.0), (186.0, 201.0), (203.0, 106.0), (100.0, 87.0), (232.0, 170.0), (248.0, 154.0), (257.0, 142.0), (123.0, 132.0), (134.0, 150.0), (169.0, 235.0), (140.0, 158.0)]
#Person-Features
#features = [(156.0, 186.0), (148.0, 273.0), (90.0, 158.0), (216.0, 21.0), (170.0, 65.0), (161.0, 102.0), (161.0, 93.0), (158.0, 68.0), (131.0, 195.0), (161.0, 116.0), (159.0, 288.0), (160.0, 86.0), (151.0, 19.0), (156.0, 168.0), (151.0, 26.0), (165.0, 289.0), (150.0, 39.0), (166.0, 214.0), (178.0, 66.0), (159.0, 78.0), (156.0, 181.0), (166.0, 199.0), (209.0, 50.0), (76.0, 153.0), (160.0, 190.0), (156.0, 63.0), (103.0, 174.0), (127.0, 192.0), (94.0, 167.0), (205.0, 60.0), (156.0, 283.0), (66.0, 153.0), (143.0, 195.0), (158.0, 243.0), (153.0, 279.0), (111.0, 180.0), (81.0, 155.0), (152.0, 54.0), (162.0, 226.0), (115.0, 184.0), (151.0, 188.0), (192.0, 65.0), (214.0, 30.0), (156.0, 152.0), (155.0, 146.0), (151.0, 46.0), (159.0, 237.0), (155.0, 250.0), (151.0, 260.0), (213.0, 39.0)]
#features = [(156.0, 186.0), (148.0, 273.0), (90.0, 158.0), (216.0, 21.0), (170.0, 65.0), (161.0, 102.0), (161.0, 93.0), (158.0, 68.0), (131.0, 195.0), (161.0, 116.0)]
count = len(features)
img = cv.LoadImage("hand.jpg")
nodes = []
searchDistance = 20

#Zuordnung Features zu Knoten 
for i in range(count):
    nodes.append(Node(features,i))
    
nodes = DFS(nodes,searchDistance)

#######Pfade zeichnen, die mit DFS gefunden wurden#######
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
            
#######END OF Pfade zeichnen########

for n in nodes:
    print "Knoten", n.nodenumber, "ist in Komponente", n.component
#Idee: Alle Komponenten mit Komponente 0 verbinden.
#Ansatz: 	Jede Komponente (außer die erste) einzelnd durchgehen und die Kürzeste Verbindung 
#			zwischen einem offenen Ende der Komponente und einem offenen Ende einer anderen Komponente
#			suchen. Dann die Komponenten vereinen. Nachdem alle Komponenten bearbeitet wurden ist sind
#			alle Komponenten miteinander verbunden. -> Pixelkonnektivität

OpenEnds = []
OpenEnds = GetOpenEnds(nodes)
NumComps = NumComponents(OpenEnds)

#Offene Enden einzeichnen
for n in OpenEnds:
    #if n.predecessor == "nil":
      #cv.Circle(img,(int(n.feature[0]),int(n.feature[1])),5,(255,0,255),thickness=2)
#  if n.postdecessor == "nil":
#    cv.Circle(img,(int(n.feature[0]),int(n.feature[1])),5,(0,255,255),thickness=2)
  if n.predecessor == "nil" and n.postdecessor == "nil":
   cv.Circle(img,(int(n.feature[0]),int(n.feature[1])),5,(255,255,0),thickness=2)
  

for i in range(NumComps): #Jede Komponente nacheinander durchgehen
     if i > 0: # Komponente 0 ist Referenz-Komponente. (Schleife könnte auch bei 1 beginnen statt bei 0.)
        print "Bearbeite Komponente", i 
        OpenEndsInComponentToConnect = GetNodesWithComponent(OpenEnds,i)# Offene Enden aus der zur Zeit betrachteten Komponente i
        OpenEndsInOtherComponents = GetNodesWithNotComponent(OpenEnds,i)# Mögliche Verbindungsknoten zu anderen Komponenten (Knoten aus OpenEnds).
        print "Anzahl Offener Enden in Komponente",i,": ", len(OpenEndsInComponentToConnect)
        bestlink = (0,"nil") #Kürzeste Verbindung zu einer anderen Komponente
        ConnectNode = "nil" #Knoten der aktuellen Komponente, mit dem die Verbindung eingegangen wird.
        for n in OpenEndsInComponentToConnect: # Alle Kandidaten durchgehen und die beste Verbindung waehlen.
            print "Bearbeite Knoten ", n.nodenumber
            PossibleLink = findNextFeature(n,OpenEndsInOtherComponents) # Kürzeste Verbindung vom aktuellen Knoten zu einer anderen Komponente
            print "Naechstgelegenes offenes Ende von ",n.nodenumber," ist Knoten ", PossibleLink[1].nodenumber, " aus Komponente ", PossibleLink[1].component, ". Distanz: ", PossibleLink[0]
            if bestlink[1] is "nil" or bestlink[0]>PossibleLink[0]: #Verbindung ist kurzer als alle zuvor vorgeschlagenen
                bestlink = PossibleLink                  
                ConnectNode = n
            print "..."
        #print "Beste Verbindung: ",ConnectNode.nodenumber," --> ", PossibleLink[1].nodenumber,"."  
        print "Beste Verbindung: ",ConnectNode.nodenumber," --> ", bestlink[1].nodenumber,"."                
        print "TODO: Verbinde Knoten ", ConnectNode.nodenumber, " mit Knoten ", bestlink[1].nodenumber, "."
        cv.Line(img, (int(ConnectNode.feature[0]),int(ConnectNode.feature[1])),(int(bestlink[1].feature[0]),int(bestlink[1].feature[1])), (0,255,0), thickness=2, lineType=8, shift=0)
        print "-------->  Damit ist Komponente", ConnectNode.component, " mit Komponente ", bestlink[1].component, " verbunden."
        for n in OpenEndsInComponentToConnect: # Update der Komponente für die OpenEnds der aktuellen Komponente (semantisch wichtig. Kein suggar.)
            n.setComponent(bestlink[1].component)
        print "-._.-._._.-._.-._.-._.-._.-._.-._."
#suggar+Kontrolle der Konnektivitaet
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


cv.SaveImage("dfs-endergebnis-hand2.png",img)
cv.ShowImage("Image",img)
cv.WaitKey()
