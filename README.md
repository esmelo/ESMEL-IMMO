# ESMEL-IMMO
# 🏠 Estimateur de Prix Immobilier - Machine Learning

Ce projet est une application web interactive permettant d'estimer le prix d'un bien immobilier en temps réel. Il utilise un modèle de Machine Learning entraîné sur le dataset "California Housing" et propose une interface utilisateur intuitive.

# Fonctionnalités
- Estimation Instantanée : Calcul du prix basé sur 8 critères (revenu, âge, pièces, localisation, etc.).
- Double Devise : Affichage du résultat en *Dollars ($)* et en *Franc CFA (XOF)*.
- Interface Fluide : Utilisation de colonnes et de sliders pour une expérience utilisateur moderne.
- Modèle Pré-entraîné : Chargement rapide du modèle via Joblib (pas de ré-entraînement nécessaire au lancement).

# Stack Technique
- Langage : Python 3.x
- Machine Learning : Scikit-Learn (Random Forest Regressor)
- Interface Web : Streamlit
- Traitement de données : Pandas, Numpy
- Persistance du modèle : Joblib

# Structure du Projet
- `esmelimmobilier.py` : Le code de l'interface utilisateur Streamlit.
- `esmel.py` : Script pour entraîner l'IA et générer le fichier du modèle.
- `esmel_modele.joblib` : Le "cerveau" de l'IA sauvegardé et compressé.
- `requirements.txt` : Liste des bibliothèques nécessaires au déploiement.

