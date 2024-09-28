import json,requests,random
from flask import Flask
from flask import render_template
# creates a Flask application
app = Flask(__name__)
def get_pokemon():
    POKEMON_API = "https://pokeapi.co/api/v2/pokemon"
    LIMIT = 5
    url = f"{POKEMON_API}?limit={LIMIT}"
    url2 = f"{POKEMON_API}"
    response = requests.get(url2)
    data = response.json()
    print(data)

    response = requests.get(url)
    data = response.json()
    return render_template('index.html',message=data)
@app.route("/")
def serve_pokemon():
    data = "hello"
    return render_template('index.html',message=data)

@app.route("/random")
def serve_random_pokemon():
    data = "random pokemon"
    return render_template('index.html',message=data)

if __name__ == "__main__":
    app.run()