"""

@author: Sandra Schroeder

Idee: Alle Komponenten mit Komponente 0 verbinden.
Ansatz: Jede Komponente (ausser die erste) einzelnd durchgehen 
und die Kuerzeste Verbindung zwischen einem offenen Ende der Komponente 
und einem offenen Ende einer anderen Komponente
suchen. Dann die Komponenten vereinen. Nachdem alle Komponenten bearbeitet 
wurden ist sind alle Komponenten miteinander verbunden. 
"""

#features: Die berechneten Features auf dem Skelett
#img: Originalbild von dem das Skelett berechnet wurde
#searchDistance: Suchdistanz. Definiert Intervall, in dem nach dem
                  #naechsten Nachbar gesucht wird.

#######BEGINN: Erste Verarbeitungsstufe. Ausfuehren der Tiefensuche.####### 
#Zuordnung Features zu Knoten 
nodes = []
for i in range(len(features)):
    #Speichern der Knoten in einer Liste nodes
    #Node bezeichnet eine Klasse. Featurepunkte werden wie Knoten in
    #einem Graphen behandelt.
    nodes.append(Node(features,i))
#Die Tiefensuche 
nodes = DFS(nodes,searchDistance)
#Pfade zeichnen, die mit der Tiefensuche gefunden wurden. 
drawDFSPath(nodes,img)
#######ENDE: Erste Verarbeitungsstufe#######

#######BEGINN: Zweite Verarbeitungsstufe. Verbinden der Zusammenhangskomponenten#######
OpenEnds = []
#Endpunkte der Zusammenhangskomponenten finden
OpenEnds = GetOpenEnds(nodes)
#Wieviele Zusammenhangskomponenten gibt es
NumComps = NumComponents(OpenEnds)
  
#Jede Komponente nacheinander durchgehen
for i in range(NumComps): 
     #Komponente 0 ist Referenz-Komponente.
     if i > 0: 
       #Offene Enden aus der zur Zeit betrachteten Komponente i
       OpenEndsInComponentToConnect = GetNodesWithComponent(OpenEnds,i)
       #Moegliche Verbindungsknoten zu anderen Komponenten (Knoten aus OpenEnds)
       #ungleich der akutellen Komponente
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
         cv.Line(img, (int(ConnectNode.feature[0]),int(ConnectNode.feature[1])),    
                 (int(bestlink[1].feature[0]),int(bestlink[1].feature[1])), 
                 (0,255,0), thickness=2, lineType=8, shift=0)
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