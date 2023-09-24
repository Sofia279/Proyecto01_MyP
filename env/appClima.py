from flask import Flask, request, jsonify, render_template
from getData import get_cache

app = Flask(__name__)

# Ruta para la URL raíz ("/")
@app.route('/', methods=['GET', 'POST'])
def index():
    data = get_cache('dataset2.csv')
    ticket = data[1]
    datos_clima = None

    if request.method == 'POST':
        ciudad = request.form['ciudad']
        datos_clima = data[0].get(ciudad)
 
        ticket_num = request.form['ticket']
        # ciudades = ticket_data.get(ticket_num) 
        ciudades = ticket.get(ticket_num)  # Corrección aquí
        if ciudades:
            ciudad_origen = ciudades[0]
            ciudad_destino = ciudades[1]
            datos_clima_origen = data[0].get(ciudad_origen)
            datos_clima_destino = data[0].get(ciudad_destino)


        """
        ticket = request.form['ticket']
        ciudades = ticket[ticket]
        ciudad_origen = ciudades[0]
        ciudad_destino = ciudades[1]
        datos_clima_origen = data[0].get(ciudad_origen)
        datos_clima_destino = data[0].get(ciudad_destino)
        """


    return render_template('index.html', datos_ciudad = datos_clima, num_ticket = ticket)
    # {{datos_ciudad}} en index

if __name__ == '__main__':
    app.run(debug=True)