import random
from flask import Flask, jsonify, render_template, request
from Cacho import CachoGame
app = Flask(__name__)

# Ruta principal para mostrar la página del juego
@app.route("/")
def index():
    return render_template("cacho.html")

# Ruta para procesar la solicitud de lanzamiento de dados y devolver los resultados
@app.route("/lanzar_dados", methods=["POST"])
def lanzar_dados():
    dados = []
    for i in range(5):
        dados.append(random.randint(1,6))
    return jsonify(dados)

# Ruta para procesar las apuestas y verificar si son correctas o no
@app.route("/verificar_apuesta", methods=["POST"])
def verificar_apuesta():
    datos = request.get_json()
    pinta = datos["pinta"]
    cantidad = datos["cantidad"]
    dados = datos["dados"]
    dados_filtrados = [dado for dado in dados if dado == pinta or dado == 1]
    if len(dados_filtrados) >= cantidad:
        return jsonify({"resultado": "correcto"})
    else:
        return jsonify({"resultado": "incorrecto"})
    
if __name__ == "__main__":
    app.run()
