from flask import Flask, render_template, request, redirect, url_for, session
import requests
import random
from api_keys import OPEN_WEATHER_MAP_API_KEY, POKE_PASS, POKE_USER #Importar contraseñas desde el archivo generado con datos de Vault

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

USERNAME = POKE_USER
PASSWORD = POKE_PASS

@app.route('/', methods=['GET', 'POST']) #rutina de inicio de sesión
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='usuario o contraseña invalido')
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        city = request.form['city']
        pokemon_name = request.form['pokemon_name']
        pokemon_type = request.form['pokemon_type']
        operation = request.form['operation']

        if operation == 'get_pokemon_type':
            pokemon_type_info = get_pokemon_type(pokemon_name)
            return render_template('get_pokemon_type.html', city=city, pokemon_name=pokemon_name, pokemon_type=pokemon_type_info)

        elif operation == 'get_random_pokemon' or operation == 'get_longest_name_pokemon':
            random_pokemon_info = get_longest_name_pokemon(pokemon_type, operation)
            return render_template('get_random_pokemon_or_longest_name.html', pokemon_info=random_pokemon_info)

        elif operation == 'get_random_weather_pokemon':
            random_weather_pokemon_info = get_random_weather_pokemon(city)
            return render_template('dashboard.html', city=city, pokemon_name=pokemon_name, random_weather_pokemon=random_weather_pokemon_info)

    return render_template('dashboard.html')

@app.route('/get_weather_based_pokemon', methods=['GET', 'POST'])
def get_weather_based_pokemon():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        city = request.form['city']
        # Recupera Pokémon basados ​​en el clima
        weather_pokemon_info = get_random_weather_pokemon(city)
        
        # Plantilla de renderizado con nombre de ciudad e información de Pokémon basada en el clima.
        return render_template('get_weather_based_pokemon.html', city=city, weather_pokemon=weather_pokemon_info)
   
    return render_template('get_weather_based_pokemon.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def get_pokemon_type(name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
    if response.status_code == 200:
        pokemon_data = response.json()
        types = [type_['type']['name'] for type_ in pokemon_data['types']]
        return f"Types of Pokémon {name}: {', '.join(types)}"
    else:
        return "Pokémon no encontrado"


def get_current_temperature(city):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_MAP_API_KEY}")
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp'] - 273.15
        return temperature
    else:
        return None

def get_strongest_type(temperature):
    if temperature >= 30:
        return 'fire'
    elif temperature >= 20 and temperature < 30:
        return 'earth'
    elif temperature >= 10 and temperature < 20:
        return 'normal'
    elif temperature >= 0 and temperature < 10:
        return 'water'
    else:
        return 'ice'

def get_random_weather_pokemon(city):
    temperature = get_current_temperature(city)
    if temperature is not None:
        strongest_type = get_strongest_type(temperature)
        response = requests.get(f"https://pokeapi.co/api/v2/type/{strongest_type}")
        if response.status_code == 200:
            data = response.json()
            pokemon_list = data['pokemon']
            filtered_pokemon_list = [pokemon['pokemon']['name'] for pokemon in pokemon_list if any(letter.lower() in pokemon['pokemon']['name'].lower() for letter in ['i', 'a', 'm'])]
            if filtered_pokemon_list:
                random_pokemon = random.choice(filtered_pokemon_list)
                return f"Un Pokémon aleatorio del tipo más fuerte según el clima ({strongest_type}) actual en el {city}: {random_pokemon}"
            else:
                return f"No se encontró ningún Pokémon con las letras 'I', 'A' o 'M' en el nombre para el tipo más fuerte ({strongest_type})"
        else:
            return "Error al obtener datos del tipo de Pokémon"
    else:
        return "Error al obtener datos del clima"

@app.route('/get_pokemon_info', methods=['POST'])
def get_pokemon_info():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        # Pokémon tipo
        pokemon_type_info = get_pokemon_type(pokemon_name)
        # Plantilla de renderizado con nombre de Pokémon y tipo de información.
        return render_template('get_pokemon_info.html', pokemon_name=pokemon_name, pokemon_type=pokemon_type_info)

# Función para buscar un Pokémon aleatorio de un tipo específico
def get_random_pokemon(type):
    response = requests.get(f"https://pokeapi.co/api/v2/type/{type.lower()}")
    if response.status_code == 200:
        type_data = response.json()
        pokemons_type = type_data['pokemon']
        # Randomly select a Pokémon
        random_pokemon = random.choice(pokemons_type)['pokemon']['name']
        return random_pokemon
    else:
        return None

# Función para buscar Pokémon con un nombre más amplio que un determinado tipo
def get_longest_name_pokemon(type):
    response = requests.get(f"https://pokeapi.co/api/v2/type/{type.lower()}")
    if response.status_code == 200:
        type_data = response.json()
        pokemons_type = type_data['pokemon']
        # Encuentra Pokémon con el nombre más amplio
        longest_name_pokemon = max(pokemons_type, key=lambda p: len(p['pokemon']['name']))['pokemon']['name']
        return longest_name_pokemon
    else:
        return None

@app.route('/get_random_pokemon', methods=['GET', 'POST'])
def random_pokemon():
    if request.method == 'POST':
        pokemon_type = request.form['pokemon_type']
        random_pokemon = get_random_pokemon(pokemon_type)
        return render_template('random_pokemon.html', random_pokemon=random_pokemon)
    return render_template('get_random_pokemon.html')

@app.route('/get_longest_name_pokemon', methods=['GET', 'POST'])
def longest_name_pokemon():
    if request.method == 'POST':
        pokemon_type = request.form['pokemon_type']
        longest_name_pokemon = get_longest_name_pokemon(pokemon_type)
        return render_template('longest_name_pokemon.html', longest_name_pokemon=longest_name_pokemon)
    return render_template('get_longest_name_pokemon.html')

# Ruta para finalizar el programa
@app.route('/finalizar')
def finalizar():
    return render_template('finalizar.html')


if __name__ == '__main__':
    app.run(debug=True)
