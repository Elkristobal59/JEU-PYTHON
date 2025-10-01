# server.py
import sqlite3
from flask import Flask, jsonify, request

# Crée l'application serveur
app = Flask(__name__)
DATABASE_FILE = 'just_price_game.db'

def get_db_connection():
    """Crée une connexion à la base de données"""
    conn = sqlite3.connect(DATABASE_FILE)
    # Permet d'obtenir des résultats sous forme de dictionnaires
    conn.row_factory = sqlite3.Row
    return conn

# Définit une "route" : quand quelqu'un accède à l'URL '/', cette fonction s'exécute
@app.route('/results', methods=['GET'])
def get_results():
    """Récupère tous les résultats du jeu et les renvoie en JSON"""
    with get_db_connection() as conn:
        results = conn.execute('SELECT * FROM game_results').fetchall()
        # Convertit les résultats en une liste de dictionnaires pour le format JSON
        return jsonify([dict(row) for row in results])

# Nouvelle route pour AJOUTER un résultat. Elle accepte les requêtes POST.
@app.route('/add_result', methods=['POST'])
def add_result():
    """Reçoit les données d'un jeu et les enregistre dans la base de données."""
    # Récupère les données envoyées avec la requête (au format JSON)
    data = request.get_json()

    just_price = data['just_price']
    attempts = data['attempts']
    won = data['won']

    with get_db_connection() as conn:
        conn.execute('INSERT INTO game_results (just_price, attempts, won) VALUES (?, ?, ?)',
                     (just_price, attempts, won))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Result saved!'}), 201

# Lance le serveur si le script est exécuté directement
if __name__ == '__main__':
    # '0.0.0.0' rend le serveur accessible depuis d'autres machines sur le réseau
    app.run(host='0.0.0.0', port=5000, debug=True)
