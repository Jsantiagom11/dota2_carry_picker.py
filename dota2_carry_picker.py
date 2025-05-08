import requests
from flask import Flask, render_template_string, request

# CONFIGURA TU ID DE DOTA 2
PLAYER_ID = 'YOUR_ACCOUNT_ID'  # Reemplaza esto con tu ID numérico de Dota 2

# URLs de la API de OpenDota
HEROES_URL = 'https://api.opendota.com/api/heroes'
PLAYER_HERO_STATS_URL = f'https://api.opendota.com/api/players/{PLAYER_ID}/heroes'

app = Flask(__name__)

def get_hero_list():
    response = requests.get(HEROES_URL)
    return {hero['id']: hero['localized_name'] for hero in response.json()}

def get_player_hero_stats():
    response = requests.get(PLAYER_HERO_STATS_URL)
    return response.json()

def calcular_puntuacion(winrate_personal, meta_tier_score, sinergia_con_equipo, counter_score):
    return (winrate_personal * 0.4) + (meta_tier_score * 0.3) + (sinergia_con_equipo * 0.2) - (counter_score * 0.1)

def simular_meta_tier_score(hero_id):
    return 0.5  # valor ficticio

def simular_sinergia_con_equipo(hero_id):
    return 0.3  # valor ficticio

def simular_counter_score(hero_id):
    return 0.2  # valor ficticio

def obtener_mejores_carries():
    heroes = get_hero_list()
    stats = get_player_hero_stats()

    mejores_opciones = []

    for hero_data in stats:
        hero_id = hero_data['hero_id']
        games = hero_data['games']
        wins = hero_data['win']

        if games < 10:
            continue

        winrate = wins / games
        meta_score = simular_meta_tier_score(hero_id)
        sinergia = simular_sinergia_con_equipo(hero_id)
        counter = simular_counter_score(hero_id)

        score = calcular_puntuacion(winrate, meta_score, sinergia, counter)
        nombre_heroe = heroes.get(hero_id, f"Hero {hero_id}")

        mejores_opciones.append((score, nombre_heroe, winrate))

    mejores_opciones.sort(reverse=True)
    return mejores_opciones[:5]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Recomendador de Carries</title>
    <style>
        body { font-family: Arial, sans-serif; background: #111; color: #eee; text-align: center; padding: 30px; }
        .hero { background: #222; margin: 10px auto; padding: 20px; border-radius: 10px; width: 60%; }
    </style>
</head>
<body>
    <h1>Top 5 Héroes recomendados como Hard Carry</h1>
    {% for score, nombre, winrate in recomendaciones %}
    <div class="hero">
        <h2>{{ nombre }}</h2>
        <p>Puntuación: {{ '%.2f'|format(score) }}</p>
        <p>Winrate personal: {{ '%.2f'|format(winrate * 100) }}%</p>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def home():
    recomendaciones = obtener_mejores_carries()
    return render_template_string(HTML_TEMPLATE, recomendaciones=recomendaciones)

if __name__ == '__main__':
    app.run(debug=True)
