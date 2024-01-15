from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth 
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho','ano','garagem']
modelo = pickle.load(open('models/model.pkl', 'rb'))

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USER')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/sentimento/<frase>')
#@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt', to='en')
    polaridade = tb_en.sentiment.polarity
    return "Polaridade: {}".format(polaridade)

@app.route('/cotacao/', methods=['POST'])
#@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')