"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D). À COMPLÉTER.

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_le_demarrage(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app
    from predict import charger_modele

    monkeypatch.setattr("predict.MODELE", MODELE.with_name("modele-inexistant.joblib"))
    charger_modele.cache_clear()
    try:
        with pytest.raises(FileNotFoundError):
            with TestClient(app):
                pass
    finally:
        charger_modele.cache_clear()


def test_modele_non_charge_repond_503(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.delattr(app.state, "classifier", raising=False)
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json={"text": "texte valide"}).status_code == 503


@pytest.mark.parametrize("exception", [RuntimeError("panne"), ValueError("bug interne")])
def test_panne_du_modele_repond_500(monkeypatch, exception):
    from fastapi.testclient import TestClient

    from api.main import app

    class BrokenClassifier:
        model_name = "test"

        def predict(self, text):
            raise exception

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", BrokenClassifier())
        reponse = client.post("/predict", json={"text": "texte valide"})
    assert reponse.status_code == 500
    assert "bug interne" not in reponse.text


def test_classes_inattendues_refusent_le_demarrage(monkeypatch):
    from api import model

    class FakePipeline:
        classes_ = ["positive", "neutral"]

    monkeypatch.setattr(model, "charger_modele", lambda: FakePipeline())
    with pytest.raises(ValueError, match="classes de modèle inattendues"):
        model.SentimentClassifier()
