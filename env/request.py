import requests

def get_request(ciudad):
    
    # leer de ambiente
    API_KEY = '2bafbc3db97c210618e917a77bd21b1b'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    parametros = {
        'q': ciudad,
        'appid': API_KEY,
        'units': 'metric'
    }

    respuesta = requests.get(BASE_URL, params=parametros)
    datos_clima = respuesta.json()
    #return datos_clima

    print(f"Solicitando datos de la API para la ciudad: {ciudad}")
    
    respuesta = requests.get(BASE_URL, params=parametros)

    if respuesta.status_code == 200:
        datos_clima = respuesta.json()
        print(f"Respuesta de la API para la ciudad {ciudad}: {datos_clima}")
        return datos_clima
    else:
        print(f"Error al hacer la solicitud a la API para la ciudad {ciudad}")
        return None