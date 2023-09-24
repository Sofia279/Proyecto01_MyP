from request import *

def get_cache(namefile):
    cache = {}
    iata_ticket = {}
    for line in open(namefile, 'r'):
        if line[0] not in iata_ticket:
            iata_ticket[line[0]] = [line[1], line[2]]

        # num_ticket,origin,destination,origin_latitude,origin_longitude,destination_latitude,destination_longitude
        if line[1] not in cache:
            requ = get_request(line[1])    
            cache[line[1]] = requ

        if line[2] not in cache:
            requ = get_request(line[2])    
            cache[line[2]] = requ
    return [cache, iata_ticket]       

 