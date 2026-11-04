import pandas as pd
from src.predict import predict

# Création de nouvelles connexions réseau
nouvelles_connexions = pd.DataFrame([
    {
        "duration": 0.520,
        "protocol": "TCP",
        "dst_port": 22,
        "src_bytes": 1500,
        "dst_bytes": 300,
        "nb_packets": 22,
        "nb_failed_logins": 5,
        "nb_conn_same_host": 42,
        "syn_rate": 0.841
    },
    {
        "duration": 1.5,
        "protocol": "UDP",
        "dst_port": 443,
        "src_bytes": 500,
        "dst_bytes": 2000,
        "nb_packets": 10,
        "nb_failed_logins": 0,
        "nb_conn_same_host": 2,
        "syn_rate": 0.05
    }
])

# Prédiction
resultats = predict(nouvelles_connexions)

# Affichage des résultats
for i, resultat in enumerate(resultats):
    if resultat == 1:
        print(f"Connexion {i+1} : ATTAQUE détectée")
    else:
        print(f"Connexion {i+1} : Connexion NORMALE")