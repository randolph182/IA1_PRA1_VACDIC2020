from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import algoritmo

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
modelo = []

@app.route('/')
def home():
   
   return render_template('index.html')

@app.route('/calcular_modelo', methods=['POST','GET'])
@cross_origin()
def calcularModelo():
   global modelo
   if request.method == 'POST':
      x = request.json
      modelo = algoritmo.ejecutar(x['criterio'],x['seleccion'])
      return jsonify({'modelo': modelo})

@app.route('/predecir_nota', methods=['POST','GET'])
@cross_origin()
def predecir_nota():
   if request.method == 'POST':
      x = request.json
      nota = algoritmo.calcularNota(modelo,x['p1'],x['p2'],x['p3'],x['p4'])
      return jsonify({'nota': nota})


if __name__ == '__main__':
   app.run('0.0.0.0',5000,debug=True)