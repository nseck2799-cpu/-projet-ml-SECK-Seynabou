import os
import joblib
import pandas as pd

# Chemin du modèle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.joblib")

# Chargement du modèle
model = joblib.load(MODEL_PATH)

# Fonction de prédiction
def predict(df: pd.DataFrame) -> list:

    expected_columns = [
        "duration",
        "protocol",
        "dst_port",
        "src_bytes",
        "dst_bytes",
        "nb_packets",
        "nb_failed_logins",
        "nb_conn_same_host",
        "syn_rate"
    ]

    # Vérification des colonnes
    missing_columns = [
        col for col in expected_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Colonnes manquantes : {missing_columns}")

    # Prédiction
    predictions = model.predict(df[expected_columns])

    return predictions.astype(int).tolist()