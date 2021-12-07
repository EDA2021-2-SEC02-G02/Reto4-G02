"""
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
from DISClib.ADT import map as mp
from DISClib.ADT.graph import addEdge, gr

airportsfile = 'airports-utf8-small.csv'
routesfile= 'routes-utf8-small.csv'
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
    print("5- Cuantificar el efecto de un aeropuerto cerrado")

catalog = None
def optionCero(cont):
    print("\nCargando información ....")
    controller.loadData(cont,airportsfile, routesfile, citiesfile)
    numairgraph1=controller.totalairnodir(cont)
    numroutesgraph1=controller.totalroutesnodir(cont)
    numairgraph2=controller.totalairdir(cont)
    numroutesgraph2=controller.totalroutesdir(cont)
    numcities=controller.totalcities(cont)
    firstcitie=controller.firstcitie(cont)
    lastcitie=controller.lastcitie(cont)
    
    print("El numero total de aeropuestos en el grafo no dirigido es de: "+str(numairgraph1))
    print("El número total de rutas aereas en el grafo no dirigido es de: " +str(numroutesgraph1))
    print("El número total de aeropuesrtos en el grafo dirigido es de: "+str(numairgraph2))
    print("El número total de rutas aereas en el grafo dirigido es de: "+str(numroutesgraph2))
    print("El número toal de ciudades es de: "+str(numcities))
    print(firstcitie)
    print(lastcitie)

def optionOne(cont):
    listmore=controller.interconection(cont)
    for iata in lt.iterator(listmore):
        graph=cont['airports_directed']
        inbound=gr.indegree(graph,iata[0])
        outbond=gr.outdegree(graph,iata[0])
        print("Name: ")
        print("city: ")
        print("contry: ")
        print("IATA: "+str(iata[0]))
        print("connections: "+ str(iata[1]))
        print("Inbound: "+str(inbound))
        print("outbond: "+ str(outbond))

def optionTwo(cont):
    iata1=input ("Ingrese el codigo IATA del aeropuerto 1")
    iata2=input ("Ingrese el codigo IATA del aeropuerto 2")
    answer=controller.count_custeres(cont,iata1,iata2)
    print("El número de componentes conectados es de: "+str(answer[0]))
    print ("El aeropuerto 1 y el aeropuerto 2 se encuentran en el mismo componente conectado? "+str(answer[1]))


"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        cont = controller.init()
        optionCero (cont)
    elif int(inputs[0]) == 1:
        
        optionOne(cont)

    elif int(inputs[0]) == 2:
        optionTwo(cont)

    elif int(inputs[0]) == 3:
        
        ciudadInicio= input("ingrese el nombre de la ciudad: ")
        mapaID= cont["ciudades"]
        llaveID= mp.get(mapaID, ciudadInicio)["value"]

        if lt.size(llaveID) == 1:
            id= lt.firstElement(llaveID)
            city= mp.get(cont["citiesMap"],id)["value"]

        elif lt.size(llaveID)> 1:
            i=1
            for id in lt.iterator(llaveID):
                infoCiudad= mp.get(cont["citiesMap"],id)["value"]
                print(str(i)+"-"+infoCiudad["city"]+"-"+infoCiudad["country"])
                i+=1
            y= int(input("\n escoja la ciudad: "))
            city= mp.get(cont["citiesMap"],lt.getElement(llaveID,y))["value"]
        
        ciudadFinal= input("ingrese el nombre de la ciudad")
        mapaID= cont["ciudades"]
        llaveID= mp.get(mapaID, ciudadFinal)["value"]

        if lt.size(llaveID) == 1:
            id= lt.firstElement(llaveID)
            cityF= mp.get(cont["citiesMap"],id)["value"]

        elif lt.size(llaveID)> 1:
            i=1
            for id in lt.iterator(llaveID):
                infoCiudad= mp.get(cont["citiesMap"],id)["value"]
                print(str(i)+"-"+infoCiudad["city"]+"-"+infoCiudad["country"])
                i+=1
            y= int(input("\n escoja la ciudad: "))
            cityF= mp.get(cont["citiesMap"],lt.getElement(llaveID,y))["value"]
     
    
    elif int(inputs[0]) == 4:
        optionFour(cont)

    elif int(inputs[0]) == 5:
        optionFive(cont)

    else:
        sys.exit(0)
sys.exit(0)
