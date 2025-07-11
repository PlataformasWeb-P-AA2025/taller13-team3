from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'una-clave-secreta-000001'

token = '5206b7adb1e37217cc460bc7c7eb2a7fb23ec289'

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

@app.route("/")
def hello_world():
    return "<p>Hola mundo</p>"

@app.route("/los/edificios")
def los_edificios():
    r = requests.get("http://localhost:8000/api/edificios/",
            auth=('santi', 'holamundo123'))
    edificios = json.loads(r.content)['results']
    numero_edificios = json.loads(r.content)['count']
    return render_template("losedificios.html", edificios=edificios,
                           numero_edificios=numero_edificios)

@app.route("/los/departamentos")
def los_departamentos():
    r = requests.get("http://localhost:8000/api/departamentos/", headers=headers)
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']

    datos2 = []
    for d in datos:
        datos2.append({
            'nombre_propietario': d['nombre_propietario'],
            'costo': d['costo'],
            'numero_cuartos': d['numero_cuartos'],
            'edificio': obtener_edificio_nombre(d['edificio'])
        })

    return render_template("losdepartamentos.html", datos=datos2,
                           numero=numero)


def obtener_edificio_nombre(url):
    r = requests.get(url, headers=headers)
    nombre_edificio = json.loads(r.content)['nombre']
    return nombre_edificio


@app.route("/crear_edificio", methods=['GET', 'POST'])
def crear_edificio():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'direccion': request.form['direccion'],
            'ciudad': request.form['ciudad'],
            'tipo': request.form['tipo'],
        }

        r = requests.post("http://localhost:8000/api/edificios/",
                          json=data, headers=headers)

        nuevo = json.loads(r.content)
        flash(f"Edificio '{nuevo['nombre']}' creado exitosamente!", 'success')
        return redirect(url_for('los_edificios'))

    return render_template("crear_edificio.html")


@app.route("/crear_departamento", methods=['GET', 'POST'])
def crear_departamento():
    # Obtener edificios disponibles
    r_edificios = requests.get("http://localhost:8000/api/edificios/", headers=headers)
    edificios_disponibles = json.loads(r_edificios.content)['results']

    if request.method == 'POST':
        data = {
            'nombre_propietario': request.form['nombre_propietario'],
            'costo': request.form['costo'],
            'numero_cuartos': request.form['numero_cuartos'],
            'edificio': request.form['edificio'],  # La URL del edificio
        }

        r = requests.post("http://localhost:8000/api/departamentos/",
                          json=data, headers=headers)

        nuevo = json.loads(r.content)
        flash(f"Departamento creado exitosamente para {nuevo['nombre_propietario']}!", 'success')
        return redirect(url_for('los_departamentos'))

    return render_template("crear_departamento.html",
                           edificios=edificios_disponibles)


if __name__ == "__main__":
    app.run(debug=True)
