# Semaine 6 : le paquet, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi le modèle n'est-il pas dans la roue ? Comment le paquet le trouve-t-il ?

Le modèle est volontairement absent de la roue : il est volumineux, dépend des
données d'entraînement et doit pouvoir être remplacé. Le paquet cherche le
modèle dans `models/sentiment.joblib` par défaut, ou à l'emplacement indiqué
par `SENTIMENT_MODELE`.

## 2. Qu'est-ce qui a changé dans api/model.py quand predict() est entré dans le paquet, et pourquoi est-ce mieux ?

`api/model.py` importe désormais `charger_modele` et `predict` depuis
`sentiment_app.predict`, sans modifier `sys.path`. Le paquet devient installable
et l'API utilise le même code que la commande `sentiment`.

## 3. La roue installée hors du dépôt : qu'a-t-il fallu lui fournir, et pourquoi scikit-learn est-il épinglé dans pyproject.toml ?

Une installation hors du dépôt doit recevoir la roue et ses dépendances, puis
le chemin du modèle via `SENTIMENT_MODELE`. scikit-learn est borné à la série
1.5, car le modèle joblib a été entraîné avec cette version et sa compatibilité
de chargement doit être conservée.
