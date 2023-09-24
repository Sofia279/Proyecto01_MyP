from aereopuerto import Aereopuerto
from clima import Clima
from clima2 import obtener_clima


def main():
    aereopuerto1 = Aereopuerto("TLC", 19.3371, -99.566)  
   # aereopuerto2 = Aereopuerto("MTY",  25.7785,-100.107) 
    cache = Clima(181)
    cache.manejar_cache()
    print (cache.obtener_vuelo("kw9f0kwvZJmsukQy"))
main()


#kw9f0kwvZJmsukQy,TLC,MTY,19.3371,-99.566,25.7785,-100.107
