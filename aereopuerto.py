class Aereopuerto: 
    def __init__(self, nombre, lat, longi) -> None:
        self.nombre = nombre
        self.lat = lat
        self.longi = longi
    
    def __hash__(self) -> int:
        valor = 0
        for c in self.nombre:
            valor += ord(c)
        return valor
        
        