import pandas as pd
from src.predict import predict

# Données de test
donnees = pd.DataFrame([
    {
        "duration": 2.5,
        "protocol": "TCP",
        "dst_port": 443,
        "src_bytes": 1500,
        "dst_bytes": 3000,
        "nb_packets": 20,
        "nb_failed_logins": 0,
        "nb_conn_same_host": 5,
        "syn_rate": 0.02
    },
    {
        "duration": 15.0,
        "protocol": "TCP",
        "dst_port": 22,
        "src_bytes": 100,
        "dst_bytes": 50,
        "nb_packets": 100,
        "nb_failed_logins": 5,
        "nb_conn_same_host": 30,
        "syn_rate": 0.8
    }
])

# Effectuer les prédictions
resultats = predict(donnees)

# Afficher les résultats
for i, resultat in enumerate(resultats, start=1):
    if resultat == 1:
        print(f"Connexion {i} : ATTAQUE détectée")
    else:
        print(f"Connexion {i} : Connexion NORMALE")