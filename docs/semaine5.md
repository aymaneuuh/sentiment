# Semaine 5 : l'interface, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface reste séparée de l'API : elle ne contient ni la logique de
prédiction ni le chemin du modèle. Elle appelle uniquement `ui.client`, ce qui
permet de faire évoluer l'interface sans dupliquer le modèle et de tester les
deux parties séparément.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Quand la confiance est sous le seuil, l'interface affiche « Je ne sais pas :
à faire vérifier par un humain » et la confiance, ainsi qu'un message
expliquant l'abstention. C'est préférable à un verdict forcé, car une
prédiction incertaine n'est pas présentée comme une décision fiable.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Si l'API tombe, l'interface affiche « API injoignable : lancez d'abord
uvicorn api.main:app » au lieu de planter. Avec `data/avis_exemple.csv`, le
résumé mesuré est `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}` :
un avis part donc vers un humain.
