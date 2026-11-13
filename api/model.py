"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de sentiment_app.predict, qui charge models/sentiment.joblib une seule fois.
"""
from typing import Literal, TypedDict

from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict

ApiLabel = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
LABELS: dict[str, Literal["POSITIVE", "NEGATIVE"]] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}
SEUIL_ABSTENTION = 0.60


class SentimentPrediction(TypedDict):
    label: ApiLabel
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()  # échoue immédiatement si le joblib manque
        classes = {str(label).lower() for label in getattr(pipeline, "classes_", [])}
        if classes != set(LABELS):
            raise ValueError(f"classes de modèle inattendues : {sorted(classes)}")

    def predict(self, text: str) -> SentimentPrediction:
        """Renvoie l'étiquette du contrat, le score et un aperçu du texte."""
        r = _predict(text)
        label: ApiLabel = LABELS[r["label"]]
        if r["score"] < SEUIL_ABSTENTION:
            label = "INDETERMINE"
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
