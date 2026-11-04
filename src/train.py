import os
import json
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score
)
# Définition des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "flux_train.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Création du dossier models
os.makedirs(MODEL_DIR, exist_ok=True)

# Chargement des données
df = pd.read_csv(DATA_PATH)

# Affichage des informations générales
print("Dimensions du dataset :", df.shape)

print("\nAperçu des données :")
print(df.head())

print("\nValeurs manquantes :")
print(df.isnull().sum())

print("\nRépartition des classes :")
print(df["attaque"].value_counts())

# Séparation des variables
X = df.drop(columns=["attaque"])
y = df["attaque"]

# Définition des variables numériques et catégorielles
numeric_features = [
    "duration",
    "dst_port",
    "src_bytes",
    "dst_bytes",
    "nb_packets",
    "nb_failed_logins",
    "nb_conn_same_host",
    "syn_rate"
]

categorical_features = ["protocol"]

# Séparation des données en entraînement et test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Vérification
print("\nDimensions des données d'entraînement :", X_train.shape)
print("Dimensions des données de test :", X_test.shape)
print("\nRépartition des attaques dans l'entraînement :")
print(y_train.value_counts())

print("\nRépartition des attaques dans le test :")
print(y_test.value_counts())

# Prétraitement des variables numériques
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Prétraitement des variables catégorielles
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# Regroupement des prétraitements
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

print("\nPrétraitement des données configuré avec succès.")
# Définition des modèles
models = {
    "Régression logistique": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),

    "Arbre de décision": DecisionTreeClassifier(
        random_state=42,
        class_weight="balanced"
    )
}

# Entraînement et évaluation
best_model = None
best_f1 = 0
best_model_name = ""

for name, classifier in models.items():

    print(f"\n========== {name} ==========")

    # Création du pipeline complet
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

    # Entraînement
    model.fit(X_train, y_train)

    # Prédictions
    y_pred = model.predict(X_test)

    # Calcul du F1-score pour la classe attaque
    score = f1_score(y_test, y_pred, pos_label=1)

    print("F1-score (attaque) :", round(score, 4))

    print("\nRapport de classification :")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["Normal", "Attaque"],
        zero_division=0
    ))

    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    # Sélection du meilleur modèle
    if score > best_f1:
        best_f1 = score
        best_model = model
        best_model_name = name

print("\n========== MEILLEUR MODÈLE ==========")
print("Modèle sélectionné :", best_model_name)
print("Meilleur F1-score :", round(best_f1, 4))
# Réentraînement du meilleur modèle sur toutes les données
best_model.fit(X, y)

# Enregistrement du modèle
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

joblib.dump(best_model, MODEL_PATH)

print("\nModèle final entraîné sur toutes les données.")
print("Modèle enregistré dans :", MODEL_PATH)
