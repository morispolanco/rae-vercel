from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Cargar variables de entorno
load_dotenv()

# Obtener la clave API desde las variables de entorno
api_key = os.getenv('API_KEY')

def hacer_consulta(pregunta):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": f"sk-tune-{api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": "Eres un académico de la lengua española que resuelve dudas y dificultades sobre esta lengua en forma exhaustiva y amable."
            },
            {
                "role": "user",
                "content": pregunta
            }
        ],
        "model": "meta/llama-3.1-405b-instruct",
        "stream": False,
        "frequency_penalty": 0.3,
        "max_tokens": 9000
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        return f"Error al hacer la consulta: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/consulta', methods=['POST'])
def consulta():
    pregunta = request.json['pregunta']
    respuesta = hacer_consulta(pregunta)
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True)
