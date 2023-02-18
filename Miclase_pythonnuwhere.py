from flask import Flask, request, jsonify
from datetime import datetime
import sklearn
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
app.config['DEBUG'] = True

root = "/home/MiguelC/Application_API/modelo_clase/" # Ruta a la carpeta donde esté el modelo guardado
root_db = "/home/MiguelC/Application_API/databases/"
model = pickle.load(open(root + 'advertising.model', 'rb'))
print(model.coef_)

@app.route('/', methods=['GET'])
def home():
	return "<h1>Miguel dale candela</h1><p>Esta es la api para predecir una predicción predictiva</p>"

# POST {"TV":, "radio":, "newspaper":} -> It returns the sales prediction for input investments
@app.route('/predict', methods=['POST'])
def get_predict():

    # Get current time for the PREDICTIONS table
    str_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Establish SQLITE3 connection and create a cursor to operate upon the DB
    connection = sqlite3.connect(root_db + "advertising.db")
    cursor = connection.cursor()

    # Get POST JSON data
    data = request.get_json()
    tv = data.get("TV",0)
    radio = data.get("radio",0)
    newspaper = data.get("newspaper",0)

    # Model prediciton
    pred = model.predict(np.array([[tv, radio, newspaper]]))[0]

    # Save prediction in PREDICTIONS table
    cursor.execute("INSERT INTO PREDICTIONS VALUES(?,?,?,?,?)", (str_time, tv, radio, newspaper, pred))
    connection.commit()
    connection.close()
    # Return the prediction
    return str(pred), 200

@app.route('/review_predicts', methods=['GET'])
def return_predicts():
      conn = sqlite3.connect(root_db + "advertising.db")
      crs = conn.cursor()
      query = "SELECT * FROM PREDICTIONS"
      resultado = jsonify(crs.execute(query).fetchall())
      conn.close()
      return resultado