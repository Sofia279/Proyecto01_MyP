from flask import Flask, request, jsonify, render_template
import requests
import time
import threading

app = Flask(__name__)

API_KEY = 'e7a2c6c0cf067883cccdd166d5357e9e'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

cache = {}  # Caché global para almacenar los datos climáticos

def obtener_clima(ciudad):
    parametros = {
        'q': ciudad,
        'appid': API_KEY,
        'units': 'metric'
    }
    respuesta = requests.get(BASE_URL, params=parametros)
    datos_clima = respuesta.json()
    return datos_clima

def manejar_cache(ciudad):
    if ciudad not in cache:
        datos_ciudad = obtener_clima(ciudad)
        cache[ciudad] = datos_ciudad
        time.sleep(60)  # Esperar para cumplir con la limitación de OpenWeatherMap

# Ruta para la URL raíz ("/")
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        datos_clima = obtener_clima(ciudad)

        return render_template('index.html', datos_clima=datos_clima)

    return render_template('index.html')

# Ruta para obtener datos climáticos
@app.route('/clima', methods=['GET'])
def obtener_clima2():
    ciudad = request.args.get('ciudad', '')

    if not ciudad:
        return jsonify({'error': 'Debes proporcionar una ciudad válida'}), 400

    # Verificar si los datos climáticos ya están en caché
    if ciudad in cache:
        datos_ciudad = cache[ciudad]
    else:
        # Si no están en caché, iniciar un hilo para obtenerlos
        hilo = threading.Thread(target=manejar_cache, args=(ciudad,))
        hilo.start()
        datos_ciudad = {'message': 'Datos climáticos en proceso de obtención'}

        # Modificar la respuesta JSON para incluir solo los datos deseados
    respuesta_json = {
        'temperatura': datos_ciudad.get('main', {}).get('temp', 'No disponible'),
        'humedad': datos_ciudad.get('main', {}).get('humidity', 'No disponible'),
        'descripcion_clima': datos_ciudad.get('weather', [{}])[0].get('description', 'No disponible')
    }    

    return jsonify(respuesta_json)

if __name__ == '__main__':
    app.run(debug=True)