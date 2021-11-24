﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import threading

airportsfile = 'airports_full.csv'
routesfile= 'routes_full.csv'
citiesfile='worldcities.csv'

initialStation = None
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Encontrar puntos de interconexión aérea ")
    print("2- Encontrar clústeres de tráfico aéreo" )
    print("3- Encontrar la ruta más corta entre ciudades")
    print("4- Utilizar las millas de viajero")
    print("5- CUantificar el efecto de un aeropuerto cerrado")

catalog = None
def optionCero(cont):
    print("\nCargando información ....")
    cont=controller.init()
    controller.loadData(cont,airportsfile, routesfile, citiesfile)
    numairgraph1=controller.totalairnodir(cont)
    numroutesgraph1=controller.totalroutesnodir(cont)
    numairgraph2=controller.totalairdir(cont)
    numroutesgraph2=controller.totalroutesdir(cont)
    numcities=controller.totalcities(cont)




"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        cont = controller.init()
        optionCero (cont)
    elif int(inputs[0]) == 1:
        optionOne(cont)

    elif int(inputs[0]) == 2:
        optionTwo(cont)

    elif int(inputs[0]) == 3:
        optionThree(cont)
    
    elif int(inputs[0]) == 4:
        optionFour(cont)

    elif int(inputs[0]) == 5:
        optionFive(cont)

    else:
        sys.exit(0)
sys.exit(0)
