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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    analyzer=model.newAnalizer()
    return analyzer


# Funciones para la carga de datos

def loadDataAirp (analyzer, airportsfile):
    airportsfile=cf.data_dir+airportsfile
    input_file =csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    lastairport = None
    for airport in input_file:
        if lastairport is not None:
            sameairport = lastairport['IATA'] == airport['IATA']
            #de aquí
            if sameairport and samedirection and not samebusStop:
                #hasta aquí
                model.addStopConnection(analyzer, lastservice, airport)
        lastservice = service
    model.addRouteConnections(analyzer)
    return analyzer
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
