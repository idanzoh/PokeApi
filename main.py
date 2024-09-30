import json,requests,random,os.path
from flask import Flask,render_template

BASE_API_URL = "https://pokeapi.co/api/v2/pokemon"
POKEMON_LIMIT = 151
CACHE_FILE = 'cache.json'

def fetch_pokemon_data(url):
    response = requests.get(url)
    return response.json()

def get_random_pokemon():
    url = f"{BASE_API_URL}?limit={POKEMON_LIMIT}"
    pokemon_list = fetch_pokemon_data(url)["results"]
    random_pokemon = random.choice(pokemon_list)
    return fetch_pokemon_data(random_pokemon["url"])

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_to_cache(pokemon_data):
    cache = load_cache()
    pokemon_name = pokemon_data['name']
    if pokemon_name not in cache:
        cache[pokemon_name] = pokemon_data
        
        with open(CACHE_FILE, 'w') as file:
            json.dump(cache, file, indent=4)

def extract_pokemon_info(pokemon_data):
    pokemon_name = pokemon_data['name']
    pokemon_img = pokemon_data['sprites']['front_default']
    pokemon_types = pokemon_data['types'][0]['type']['name']

    return {
        "name": pokemon_name,
        "img": pokemon_img,
        "types": pokemon_types
    }

# creates a Flask application
app = Flask(__name__)

@app.route("/")
def serve_random_pokemon():
    cache = load_cache()
    pokemon_data = get_random_pokemon()
    pokemon_info = extract_pokemon_info(pokemon_data)

    pokemon_name = pokemon_info['name']
    if pokemon_name in cache:
        pokemon_info = cache[pokemon_name]
    else:
        save_to_cache(pokemon_info)
    return render_template('index.html', poke_name=pokemon_info['name'].capitalize(),poke_img=pokemon_info['img'],poke_type=pokemon_info['types'].capitalize())

if __name__ == "__main__":
    app.run()

