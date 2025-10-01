from random import randint
import requests

just_price = randint(1, 100)
running = True
attempts = 0

while running and attempts < 3:
    user_price = int(input("Entrez un prix entre 1 et 100 : "))
    attempts += 1
    if user_price == just_price:
        print("Gagné !")
        running = False
    elif user_price < just_price:
        print("C'est plus !")
    else:
        print("C'est moins !")  

# Une fois la boucle terminée, on détermine si le joueur a gagné
won = not running

# On affiche le message de fin de partie approprié
if won:
    print("Bravo ! Le juste prix était bien", just_price)
else:
    print("Perdu ! Le juste prix était", just_price)

print("--- Enregistrement du score ---")

# Prépare les données à envoyer au serveur
game_data = {
    "just_price": just_price,
    "attempts": attempts,
    "won": won
}

# IMPORTANT : Remplacez "IP_DU_SERVEUR" par l'adresse IP que vous avez trouvée à l'étape 1.
server_url = "http://10.5.0.2:5000/add_result"

try:
    # On ajoute un timeout de 5 secondes. Si le serveur ne répond pas, on arrête d'attendre.
    response = requests.post(server_url, json=game_data, timeout=5)
    if response.status_code == 201:
        print("Score enregistré avec succès !")
    else:
        print(f"Erreur du serveur : {response.status_code} - {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Impossible de contacter le serveur pour enregistrer le score : {e}")

print("\nMerci d'avoir joué !")
