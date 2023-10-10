from request import *

class FlightData:
    def __init__(self, namefile):
        self._cache, self._iata_ticket = self._get_cache(namefile)

    def _get_request(self, city):
        pass

    def get_cache(self, namefile):
        cache = {}
        iata_ticket = {}
        for line in open(namefile, 'r'):
            pass
        return cache, iata_ticket

    def get_flight_info(self, num_ticket):
        pass

    def get_city_info(self, iata_code):
        pass

 