
import os
import joblib
import pandas as pd

# Chemin du modèle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.joblib")

# Chargement du modèle
model = joblib.load(MODEL_PATH)

# Colonnes nécessaires pour la prédiction
EXPECTED_COLUMNS = [
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

def predict(df: pd.DataFrame) -> list:
    """Prédit si les connexions réseau sont normales ou malveillantes."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Les données doivent être un DataFrame pandas.")

    if df.empty:
        raise ValueError("Le DataFrame est vide.")

    missing_columns = [
        col for col in EXPECTED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Colonnes manquantes : {missing_columns}")

    predictions = model.predict(df[EXPECTED_COLUMNS])

    return predictions.astype(int).tolist()
