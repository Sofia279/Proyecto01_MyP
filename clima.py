import requests, time, json, csv
import math

from aereopuerto import Aereopuerto
import csv, json
import urllib
import urllib.request
import urllib.parse

from datos import Vuelo

class Clima:

    def __init__(self, size) -> None:
        self.vuelos = list()
        self.cache = [list()]
        self.size = size
        for i in range(size):
            self.cache.append(list())
    
     
    def obtener_climaIATA(self, codigo):
        i = self.buscar_aereopuerto(Aereopuerto(codigo ,0,0))
        print(i)
        if(i>-1):
            return self.filtra_datos(self.cache[i][1])
    def buscar_aereopuerto(self, aereopuerto):
        for i in range(self.size):
            if(len(self.cache[(aereopuerto.__hash__()+i)%self.size]) == 0):
                return -1 
            if(self.cache[(aereopuerto.__hash__()+i)%self.size][0]==aereopuerto.nombre):
                return (aereopuerto.__hash__()+i)%self.size
        return -1
    
    def obtener_clima(self, aereopuerto):
        i = self.buscar_aereopuerto(aereopuerto)
        if(i>-1):
            return self.filtra_datos(self.cache[i][1])
    
    def filtra_datos(self, datos):
        return datos['name'] + ", " + datos['sys']['country'] + "\n" + datos['weather'][0]['description'] + "\n" + str(math.floor(datos['main']['temp'] - 273))
    
    def buscar(self, aereopuerto):
        for i in range(self.size):
            if(len(self.cache[(aereopuerto.__hash__()+i)%self.size]) == 0):
                return False 
            if(self.cache[(aereopuerto.__hash__()+i)%self.size][0]==aereopuerto.nombre):
                return True
        return False
    
    def buscar_casilla(self, aereopuerto):
         for i in range(self.size):
            if(len(self.cache[(aereopuerto.__hash__()+i)%self.size]) == 0):
                return (aereopuerto.__hash__()+i)%self.size
         return -1

    def obtener_vuelo(self, id):
        for vuelo in self.vuelos:
            if(vuelo.id) == id:
                return self.obtener_clima(vuelo.origen)+self.obtener_clima(vuelo.destino)
            
    def peticion(self, aeropuerto):
        llave = "685b7a3831ba303b4603a5e7c8ab09be"
        url = "https://api.openweathermap.org/data/2.5/weather?lat="\
                    + str(aeropuerto.lat) + "&lon=" + str(aeropuerto.longi)\
                    + "&appid=" + llave + "&lang=es"
        archivoPeticion = urllib.request.urlopen(url,timeout=30)
        return json.loads(archivoPeticion.read())

    def manejar_cache(self):

        # Se abre el archivo csv (la base de datos) en modo lectura
        with open('dataset2.csv', 'r') as archivo:
        

            # Se ignora la primera fila (los títulos)
            next(archivo)
            lector = csv.reader(archivo)
            # Recorre el archivo fila por fila
            for fila in lector:
                aereopuerto_origen = Aereopuerto (fila[1],fila[3],fila[4])
                aereopuerto_destino = Aereopuerto (fila[2],fila[5],fila[6])
                self.vuelos.append(Vuelo(fila[0],aereopuerto_origen, aereopuerto_destino))

                # Se verifica si la aereopuerto de origen ya esta en el cache
                if(not self.buscar(aereopuerto_origen)):

                    datos_aereopuerto_origen = self.peticion(aereopuerto_origen)
                    i = self.buscar_casilla(aereopuerto_origen)
                    self.cache[i] = [aereopuerto_origen.nombre, datos_aereopuerto_origen]
                    # Esperar un tiempo para evitar exceder la limitación de OpenWeatherMap (60 peticiones por min)
                
                # Se verifica si la aereopuerto de destino ya esta en el cache
                if(not self.buscar(aereopuerto_destino)):
                    
                    datos_aereopuerto_destino = self.peticion(aereopuerto_destino)
                    i = self.buscar_casilla(aereopuerto_destino)
                    self.cache[i] = [aereopuerto_destino.nombre, datos_aereopuerto_destino]

                    # Esperar un tiempo nuevamente
        # Devolver el caché actualizado
        return self.cache


    if __name__ == "__main__":
        cache_actualizado = manejar_cache()


    #for aereopuerto, datos in cache_actualizado.items():
    #        print("Clima actual en", aereopuerto)
    #        print("Temperatura:", datos['main']['temp'], "°C")
    #        print("Humedad:", datos['main']['humidity'], "%")
    #        print("Descripción:", datos['weather'][0]['description'])
    #        print()