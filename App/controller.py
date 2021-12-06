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
 """

import config as cf
import model
import csv
import time as time
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import addEdge, gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    analyzer=model.newAnalizer()
    return analyzer


# Funciones para la carga de datos
def loadData (analyzer, airportsfile,routesfile, citiesfile):
    loadDataAirp(analyzer,airportsfile)
    loadDataRoutes(analyzer, routesfile)
    loadDataCities(analyzer,citiesfile )
    load_tablecity(analyzer)
    return analyzer
    

def loadDataAirp (analyzer, airportsfile):
    airportsfile=cf.data_dir+airportsfile
    input_file =csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addAirportconnection(analyzer, airport)
    return analyzer
    

def loadDataRoutes (analyzer, routesfile):
    routesfile=cf.data_dir+routesfile
    input_file =csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:
        model.addRouteConnections(analyzer, route) 
    return analyzer

def loadDataCities (analyzer, citiesfile):
    citiesfile=cf.data_dir+citiesfile
    input_file =csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")
    for city in input_file:
        model.addcity(analyzer, city)
    return analyzer

def load_tablecity (analyzer):
    for city in lt.iterator (analyzer['cities']):
        id=city["id"]
        tablename=analyzer["citiesMap"]
        model.addcitymap(tablename,id,city)
        model.agregarLista(analyzer,city["city"],id)
    return analyzer



#Funciones para cansultar el número de vértices
def totalairnodir(analyzer):
    return model.totalairnodir(analyzer)

def totalroutesnodir(analyzer):
    return model.totalroutesnodir(analyzer)

def totalairdir(analyzer):
    return model.totalairdir(analyzer)

def totalroutesdir(analyzer):
    return model.totalroutesdir(analyzer)

def totalcities(analyzer):
    return model.totalcities(analyzer)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
