from cgi import print_arguments
from flask import Flask, render_template, request
from aereopuerto import Aereopuerto
from clima import Clima
from fuzzywuzzy import process
import requests

ciudades = [
    'Ciudad de México', 'Guadalajara', 'Santiago', 'Miami', 'Dallas-Fort Worth', 'Cancún', 'París', 'Lima',
    'Tampico', 'Monterrey', 'Madrid', 'Bogotá', 'Puerto Vallarta', 'Veracruz', 'Charlotte', 'Querétaro', 'Toronto',
    'Mérida', 'San Luis Potosí', 'Los Ángeles', 'Aguascalientes', 'Chetumal', 'Ixtapa-Zihuatanejo', 'Phoenix',
    'Filadelfia', 'Ciudad Juárez', 'Ámsterdam', 'Tijuana', 'Vancouver', 'Ciudad Obregón', 'Toluca', 'Huatulco',
    'Ciudad del Carmen', 'Villahermosa', 'Puerto Escondido', 'Cozumel', 'León', 'Hermosillo', 'Nueva York',
    'Belice City', 'Torreón', 'Chicago', 'Atlanta', 'Zacatecas', 'Acapulco', 'Oaxaca', 'La Habana', 'Houston',
    'Chihuahua', 'Guatemala City', 'Mazatlán'
]

ciudades_iata = {
    'MEX': 'Ciudad de México',
    'GDL': 'Guadalajara',
    'SCL': 'Santiago',
    'MIA': 'Miami',
    'DFW': 'Dallas-Fort Worth',
    'CUN': 'Cancún',
    'CDG': 'París',
    'LIM': 'Lima',
    'TAM': 'Tampico',
    'MTY': 'Monterrey',
    'MAD': 'Madrid',
    'BOG': 'Bogotá',
    'PVR': 'Puerto Vallarta',
    'VER': 'Veracruz',
    'CLT': 'Charlotte',
    'QRO': 'Querétaro',
    'YYZ': 'Toronto',
    'MID': 'Mérida',
    'SLP': 'San Luis Potosí',
    'LAX': 'Los Ángeles',
    'AGU': 'Aguascalientes',
    'CTM': 'Chetumal',
    'ZIH': 'Ixtapa-Zihuatanejo',
    'PHX': 'Phoenix',
    'PHL': 'Filadelfia',
    'CJS': 'Ciudad Juárez',
    'AMS': 'Ámsterdam',
    'TIJ': 'Tijuana',
    'YVR': 'Vancouver',
    'CEN': 'Ciudad Obregón',
    'TLC': 'Toluca',
    'HUX': 'Huatulco',
    'CME': 'Ciudad del Carmen',
    'VSA': 'Villahermosa',
    'PXM': 'Puerto Escondido',
    'CZM': 'Cozumel',
    'BJX': 'León',
    'HMO': 'Hermosillo',
    'JFK': 'Nueva York',
    'BZE': 'Belice City',
    'TRC': 'Torreón',
    'ORD': 'Chicago',
    'ATL': 'Atlanta',
    'ZCL': 'Zacatecas',
    'ACA': 'Acapulco',
    'OAX': 'Oaxaca',
    'HAV': 'La Habana',
    'IAH': 'Houston',
    'CUU': 'Chihuahua',
    'GUA': 'Guatemala City',
    'MZT': 'Mazatlán',
}

app = Flask(__name__)

cache = {}

@app.route('/', methods=['GET', 'POST'])
def mostrar_clima():
    if request.method == 'POST':
        ciudad_ingresada = request.form['ciudad']
        ciudad_encontrada = ciudades_iata.get(ciudad_ingresada)

        if not ciudad_encontrada:
            ciudad_encontrada, score = process.extractOne(ciudad_ingresada, ciudades)

            if score < 80:
                mensaje_error = f'No se pudo encontrar información del clima para "{ciudad_ingresada}". Intente ingresar otra ciudad.'
                return render_template('index.html', mensaje_error=mensaje_error)

        api_key = 'e7a2c6c0cf067883cccdd166d5357e9e'  # Reemplaza con tu clave de API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad_encontrada}&appid={api_key}&lang=es'
        response = requests.get(url)

        if response.status_code == 200:
            clima_info = response.json()
            temperatura = clima_info['main']['temp']
            humedad = clima_info['main']['humidity']
            descripcion_clima = clima_info['weather'][0]['description']
            return render_template('index.html', ciudad=ciudad_encontrada, temperatura=temperatura, humedad=humedad, descripcion_clima=descripcion_clima)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)