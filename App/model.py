"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.liststructure import addLast
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.ADT.graph import addEdge, gr
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalizer():
    try:
        analyzer={  'airports':None,
                    'airports_no_directed':None,
                    'airports_directed':None,
                    'cities_from_airport':None,
                    'cities':None,
                    'citiesMap':None
                    }
        analyzer['airports']=lt.newList("ARRAY_LIST",compareAirports)
        analyzer['airports_no_directed']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=False,
                                                    size=8996,
                                                    comparefunction=compareAirports)

        analyzer['airports_directed']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=True,
                                                    size=8996,
                                                    comparefunction=compareAirports)

     
        analyzer["cities"]= lt.newList("ARRAY_LIST",compareCities )
        
        analyzer['ciudades']=mp.newMap(37498,
                                 maptype="PROBING",
                                 loadfactor=0.89,
                                 )

        analyzer['citiesMap']=mp.newMap(37498,
                                 maptype="PROBING",
                                 loadfactor=0.89,
                                 comparefunction=comparecitiesmap)

        analyzer['citiestreelong']=om.newMap(omaptype="RBT",
                                        comparefunction=compareLongitudes)   
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def compareAirports(code, airport):
    #print (code)
    #print (airport)
    aircode=airport['key']
    if (code == aircode):
        return 0
    elif (code > aircode):
        return 1
    else:
        return -1

def compareCities(id,city):
    cityid=city['id']
    if (id == cityid):
        return 0
    elif (id > cityid):
        return 1
    else:
        return -1
    
def comparecitiesmap (keycity,city):
    cityentry=me.getKey(city)
    if (keycity==cityentry):
        return 0
    elif (keycity>cityentry):
        return 1
    else:
        return -1

def compareLongitudes(Long1, Long2):
    Long1=float(Long1)
    Long2=float(Long2)
    if (Long1==Long2):
        return 0
    elif (Long1 > Long2):
        return 1
    else:
        return -1

def addairportlist (analyzer, airport):
    airportl={
           "IATA":airport["IATA"],
           "Name":airport["Name"],
           "City":airport["City"],
           "Country":airport["Country"],
           "id":airport["id"],
           "Latitude":airport["Latitude"],
           "Longitude":airport["Longitude"]
            }
    lt.addLast(analyzer["airports"], airportl)

# Funciones para agregar informacion al catalogo
def agregarLista (analyzer,city,id):
    try:
        mapa = analyzer['ciudades']
        if city != "" and mp.contains(mapa, city)==False:
            listaCiudades=lt.newList("ARRAY_LIST")
            lt.addLast(listaCiudades,id)
            mp.put (mapa, city, listaCiudades)
        
        elif  mp.contains(mapa, city)==True:
        
            temp=mp.get(mapa, city)
            tempo=me.getValue(temp)
        
            lt.addLast (tempo, id)
        return analyzer 
    except Exception as e:
        raise e

def addAirportconnection(analyzer, airport):
    try:
        origin=airport['IATA']
        addAirport(analyzer['airports_directed'], origin)
        
        #addRouteStop(analyzer, service)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportconnection')

def addAirport(graph, origin):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        #print(gr.containsVertex(analyzer['airports_directed'], origin))
        if not gr.containsVertex(graph, origin):
            gr.insertVertex(graph, origin)

        return graph
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')
        
   

def addRouteConnections(analyzer, route):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """

    try:
        origin=route['Departure']
        destination=route['Destination']
        weight=float(route['distance_km'])
        addConnection(analyzer, origin, destination, weight)
        addConnectionnodirected(analyzer,origin, destination, weight)
    except Exception as exp:
        error.reraise(exp, 'model:addRouteConnection')

def addConnection(analyzer, origin, destination,weight):
    """
    Adiciona un arco entre dos estaciones
    """
    edgedirected = gr.getEdge(analyzer['airports_directed'], origin, destination)
    if edgedirected is None:
        gr.addEdge(analyzer['airports_directed'], origin, destination,weight)
   
    return analyzer

def addConnectionnodirected (analyzer,origin, destination, weight):
    #print(analyzer['airports_no_directed'])
    edge=gr.getEdge(analyzer['airports_directed'], destination, origin)
    if edge is not None:
        addAirport(analyzer['airports_no_directed'],origin)
        addAirport(analyzer['airports_no_directed'],destination)
        edgenodirected = gr.getEdge(analyzer['airports_no_directed'], origin, destination)
        if edgenodirected is None:
            gr.addEdge(analyzer['airports_no_directed'], origin, destination,weight)
    return analyzer
        



def addcity (analyzer, city):
    city={
        "city":city["city"],
        "latitude":city["lat"],
        "longitude":city["lng"],
        "country":city["country"],
        "id":city["id"]
         }
    lt.addLast(analyzer["cities"],city)
    updateLongitude(analyzer['citiestreelong'],city)

def addcitymap(tablename, city, citylist):
    try:
        if city!= "" and mp.contains (tablename,city)==False:
            mp.put(tablename,city,citylist)
    except Exception as e:
        raise e

def updateLongitude(tree, city):
    occurredlongitude=(round(float(city["longitude"]),2))
    entry=om.get(tree,occurredlongitude)
    if entry is None:
        longitudeentry=newLatitudetree(city)
        om.put(tree,occurredlongitude,longitudeentry)
    else:
        longitudeentry=me.getValue(entry)
    addLatitudevalue(longitudeentry,city)
    return tree

def newLatitudetree(city):
    latitudes={}
    latitudes["latitudeindex"]=om.newMap (omaptype="RBT",
                                  comparefunction=compareLatitudes)
    return latitudes
    
def addLatitudevalue(tree, city):
    tree=tree["latitudeindex"]
    occurredlatitude=(round(float(city["latitude"]),2))
    entry=om.get(tree,occurredlatitude)
    if entry is None:
        latitudeentry=lt.newList("ARRAY_LISY")
        om.put(tree,occurredlatitude,latitudeentry)
    else:
        latitudeentry=me.getValue(entry)
    lt.addLast(latitudeentry,city)


def compareLatitudes (Lati1, Lati2):
    Lati1=float(Lati1)
    Lati2=float(Lati2)
    if (Lati1==Lati2):
        return 0
    elif (Lati1 > Lati2):
        return 1
    else:
        return -1
# Funciones para creacion de datos

# Funciones de consulta
def totalairnodir(analyzer):
    return gr.numVertices(analyzer['airports_no_directed'])
    
def totalroutesnodir(analyzer):
    return gr.numEdges(analyzer['airports_no_directed'])

def firstairnodir(analyzer):
    graph=analyzer['airports_no_directed']
    listnor=analyzer['airports']
    listgraph=gr.vertices(graph)
    first=lt.firstElement(listgraph)
    last=lt.lastElement(listgraph)
    for air in lt.iterator(listnor):
        if air["IATA"]==first:
            airfirst=air
        elif air["IATA"]==last:
            airlast=air
    return (airfirst,airlast)


def totalairdir(analyzer):
    return gr.numVertices(analyzer['airports_directed'])
    
def totalroutesdir(analyzer):
    return gr.numEdges(analyzer['airports_directed'])

def firstairdir(analyzer):
    graph=analyzer['airports_directed']
    listnor=analyzer['airports']
    listgraph=gr.vertices(graph)
    first=lt.firstElement(listgraph)
    last=lt.lastElement(listgraph)
    for air in lt.iterator(listnor):
        if air["IATA"]==first:
            airfirst=air
        elif air["IATA"]==last:
            airlast=air
    return (airfirst,airlast)
    
def totalcities(analyzer):
    return lt.size(analyzer['cities'])

def firstcitie(analyzer):
    list=analyzer["cities"]
    first=lt.firstElement(list)
    return first

def lastcitie(analyzer):
    list=analyzer["cities"]
    last=lt.lastElement(list)
    return last
    

# REQ 1
def interconection(analyzer):
    airplist=analyzer["airports"]
    graph=analyzer['airports_directed']
    listnodes=gr.vertices(graph)
    more=lt.newList("ARRAY_LIST")
    for air in lt.iterator(airplist):
        for node in lt.iterator(listnodes):
            if air["IATA"] == node:
                outde=gr.outdegree(graph,node)
                inde=gr.indegree(graph, node)
                total=outde+inde
                lt.addLast(more,(node,total))
    mg.sort(more,cmptotal)
    return more

def cmptotal (num1, num2):
    return num1[1]>num2[1]

# REQ 2
def count_custeres(analyzer,iata1, iata2):
    dirgraph=analyzer['airports_directed']
    sccestructure=scc.KosarajuSCC(dirgraph)
    numconected=scc.connectedComponents(sccestructure)
    strong=scc.stronglyConnected(sccestructure,iata1,iata2)
    return(numconected,strong)


# REQ 3
def find_nearairport(analyzer, cityorigin, citydestination ):
    graph_no_directed=analyzer['airports_no_directed']

    route=min_distance(analyzer,airorigin, airdestination)

def min_distance(analyzer,airorigin,airdestination):
    graph_directed=analyzer['airports_directed']
    mod_graph=djk.Dijkstra(graph_directed, airorigin)
    distance_to_airport=djk.distTo(mod_graph, airdestination)
    inside_routes=djk.pathTo(mod_graph, airdestination)
    lst_weights=lt.newList("ARRAY_LIST")
    i=1
    j=2
    while j <= lt.size(inside_routes):
        first=lt.getElement(inside_routes,i)
        second=lt.getElement(inside_routes,j)
        edge=gr.getEdge(graph_directed,first,second)
        lt.addLast(lst_weights,edge['weight'])
        i+=1 
        j+=1
    return (distance_to_airport, lst_weights)


# REQ 4

# REQ 5
def airclosed(analyzer, iata):
    outair=None
    dirgraph=analyzer['airports_directed']
    nodesgraph=gr.vertices(dirgraph)
    if iata in lt.iterator (nodesgraph):
        outair= gr.adjacents(dirgraph, iata)
    return (outair)