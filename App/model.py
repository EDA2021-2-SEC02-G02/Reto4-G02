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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import addEdge, gr
from DISClib.Algorithms.Graphs import scc
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
        analyzer={
                    'airports_no_directed':None,
                    'airports_directed':None,
                    'cities_from_airport':None,
                    'cities':None,
                    'citiesMap':None
                    }
        
        analyzer['airports_no_directed']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=False,
                                                    size=8996,
                                                    comparefunction=compareAirports)

        analyzer['airports_directed']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=True,
                                                    size=8996,
                                                    comparefunction=compareAirports)

        #analyzer['cities_from_airport']=gr.newGraph(datastructure='ADJ_LIST',
         #                                           directed=True,
         #                                           size=46494,
         #                                           comparefunction=compareCities)

        analyzer['cities']=lt.newList('ARRAY_LIST', cmpfunction=compareCities)

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

# Funciones para agregar informacion al catalogo

def addAirportconnection(analyzer, airport):
    try:
        origin=airport['IATA']
        addAirport(analyzer, origin)
        
        #addRouteStop(analyzer, service)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportconnection')

def addAirport(analyzer, origin):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        #print(gr.containsVertex(analyzer['airports_directed'], origin))
        if not gr.containsVertex(analyzer['airports_directed'], origin):
            gr.insertVertex(analyzer['airports_directed'], origin)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')
        
    #except Exception as exp:
     #   error.reraise(exp, 'model:addAirport')

def addRouteConnections(analyzer, route):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    #lststops = m.keySet(analyzer['stops'])
    try:
        origin=route['Departure']
        destination=route['Destination']
        weight=float(route['distance_km'])
        addConnection(analyzer, origin, destination, weight)
    except Exception as exp:
        error.reraise(exp, 'model:addRouteConnection')

def addConnection(analyzer, origin, destination,weight):
    """
    Adiciona un arco entre dos estaciones
    """
    edgedirected = gr.getEdge(analyzer['airports_directed'], origin, destination)
   # edgenodirected=gr.getEdge(analyzer['airports_directed'], destination, origin)
    if edgedirected is None:
        gr.addEdge(analyzer['airports_directed'], origin, destination,weight)
   #     gr.addEdge(analyzer['airports_directed'], origin, destination,weight)
   # if edgenodirected is not None:
   #     gr.addEdge(analyzer['airports_no_directed'], origin, destination,weight)
    return analyzer

def createnodirected (analyzer):
    vertices=gr.vertices(analyzer['airports_directed'])
    for vertex in lt.iterator(vertices):
        addairportnodirected(analyzer,vertex)

    i=1
    while i<= lt.size(vertices):
        j=2
        vertexa=lt.getElement(vertices,i)
        while j<= lt.size(vertices):
            vertexb=lt.getElement(vertices,j)
            edge1=gr.getEdge(analyzer['airports_directed'], vertexa,vertexb)
            if edge1!= None:
                weight=edge1['weight']
                edge2=gr.getEdge(analyzer['airports_directed'], vertexb,vertexa)
                if edge2!= None:
                    addedgenodirected(analyzer, vertexa,vertexb,weight)
            j+=1
        i+=1
        

def addairportnodirected(analyzer,vertex):
    try:
        #print(gr.containsVertex(analyzer['airports_directed'], origin))
        if not gr.containsVertex(analyzer['airports_no_directed'], vertex):
            gr.insertVertex(analyzer['airports_no_directed'], vertex)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')

def addedgenodirected(analyzer, vertexa,vertexb,weight):
    edgenodirected = gr.getEdge(analyzer['airports_no_directed'], vertexa, vertexb)
   # edgenodirected=gr.getEdge(analyzer['airports_directed'], destination, origin)
    if edgenodirected is None:
        gr.addEdge(analyzer['airports_no_directed'], vertexa, vertexb,weight)


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

def totalairdir(analyzer):
    return gr.numVertices(analyzer['airports_directed'])
    
def totalroutesdir(analyzer):
    return gr.numEdges(analyzer['airports_directed'])
    
def totalcities(analyzer):
    return mp.size(analyzer['citiesMap'])
    

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
