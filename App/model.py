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
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
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
                    'cities_from_airport':None
                    }
        analyzer['airports_no_directed']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=False,
                                                    size=10,
                                                    comparefunction=compareAirports)

        analyzer['airports_directed']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=True,
                                                    size=10,
                                                    comparefunction=compareAirports)

        analyzer['cities_from_airport']=gr.newGraph(datastructure='ADJ_LIST',
                                                    directed=True,
                                                    size=10,
                                                    comparefunction=compareCities)                                          
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def compareAirports(code, airport):
    aircode=airport['IATA']
    if (code == aircode):
        return 0
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

# Funciones para agregar informacion al catalogo

def add 
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
