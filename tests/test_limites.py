"""Tests aux limites du contrat d'entrée (TP4, étape B). À COMPLÉTER.

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


# Étape B.1 : huit cas au moins, chacun avec son code attendu. Deux sont donnés.
# À ajouter : texte fait d'espaces, un seul caractère, exactement 2000 caractères,
# champ absent, champ d'un autre type (42), corps qui n'est pas du JSON (b"pas du json").
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="texte-blanc"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="type-invalide"),
    pytest.param(b"pas du json", 422, id="corps-invalide"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        detail = reponse.json()["detail"]
        assert isinstance(detail, list)
        assert all({"loc", "msg", "type"} <= set(erreur) for erreur in detail)


@settings(deadline=None, max_examples=20)
@given(st.text(min_size=1, max_size=2000).filter(lambda texte: bool(texte.strip())))
def test_tout_texte_non_blanc_est_accepte(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    assert reponse.json()["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0 <= reponse.json()["score"] <= 1


@settings(deadline=None, max_examples=20)
@given(st.text(alphabet=st.sampled_from([" ", "\t", "\n", "\r", "\v", "\f"]),
               min_size=1, max_size=2000))
def test_tout_texte_blanc_est_refuse(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422
    detail = reponse.json()["detail"]
    assert isinstance(detail, list)
    assert all({"loc", "msg", "type"} <= set(erreur) for erreur in detail)


# Étape B.5 : deux tests de propriété avec hypothesis, dans ce fichier.
#   from hypothesis import given, settings, strategies as st
#   1. tout texte de 1 à 2000 caractères contenant un caractère non blanc :
#      200, étiquette du contrat, score entre 0 et 1 ;
#   2. tout texte fait uniquement de blancs : 422, sous la forme standard.
# Pensez à @settings(deadline=None) : le premier appel peut être plus lent que les autres.
