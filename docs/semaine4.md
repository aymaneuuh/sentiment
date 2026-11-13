# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : mesure non disponible avant l'installation du kit dans cette copie.
- Après (étape D) : 97,78 % pour `api/` (90 lignes, 2 non couvertes dans
  `api/main.py`, lignes 83-85 du bloc de lancement direct). Aucune ligne n'a été
  exclue de la mesure ; le seuil de 95 % est atteint.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Les textes composés uniquement d'espaces pouvaient atteindre le modèle | `test_frontieres_du_contrat` et `test_tout_texte_blanc_est_refuse` | Validation `field_validator` dans `PredictRequest`, avec `strip()` |
| Une `ValueError` du modèle était renvoyée comme une 422 | `test_panne_du_modele_repond_500` | Toute exception de prédiction est journalisée et renvoyée en 500 |
| Les classes d'un modèle incompatible n'étaient pas contrôlées | `test_classes_inattendues_refusent_le_demarrage` | Vérification explicite des classes au démarrage |

## 3. Seuil d'abstention

- À 0,50, le modèle répond aux 58 avis, avec 87,9 % d'exactitude et 7 erreurs.
  À 0,60, il répond à 42 avis (72 %), avec 95,2 % d'exactitude et 2 erreurs.
  À 0,70, il répond à 37 avis (64 %), avec 100 % d'exactitude et aucune erreur.
- Seuil retenu : 0,60, soit 16 avis envoyés à un humain (28 %). Ce compromis
  réduit fortement les erreurs sans abandonner trop de prédictions.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) : 7 justes, 10 abstentions et 4 erreurs
  franches déclarées sur 21 avis.
- Le modèle est prudent sur les formulations hors domaine et les avis difficiles,
  mais le jeu de démonstration reste limité : certaines négations ou formulations
  négatives sont encore classées POSITIVE.

## 5. Outils statiques

- Remarques au départ : ruff signalait 15 problèmes et mypy 3 problèmes après
  les premiers changements. Après correction : `ruff check .` et `mypy api` sont
  muets.
- Les tests de limites, les propriétés et les tests de panne ont trouvé des
  défauts de comportement que les outils statiques ne pouvaient pas détecter.
  Les outils statiques complètent donc les tests, mais ne les remplacent pas.
