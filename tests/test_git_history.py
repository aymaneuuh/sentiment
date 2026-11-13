"""Tests sur l'historique Git : un commit par membre du binôme.

Ignorés si le dossier n'est pas un dépôt Git (par exemple sur un kit fraîchement décompressé).
"""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

DEFAULT_MIN_AUTHORS = 2  # un binôme : deux auteurs de commits


def _required_min_authors() -> int:
    value = os.getenv("MIN_GIT_AUTHORS", str(DEFAULT_MIN_AUTHORS))
    try:
        return max(1, int(value))
    except ValueError:
        return DEFAULT_MIN_AUTHORS


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


@pytest.fixture(scope="module")
def git_root(root: Path) -> Path:
    if shutil.which("git") is None or not (root / ".git").exists():
        pytest.skip("pas un dépôt Git")
    try:
        _git(root, "rev-parse", "HEAD")
    except subprocess.CalledProcessError:
        pytest.skip("aucun commit")
    return root


def test_has_at_least_one_commit(git_root: Path):
    assert _git(git_root, "rev-list", "--count", "HEAD").strip() != "0"


def test_each_member_has_committed(git_root: Path):
    out = _git(git_root, "shortlog", "-sn", "--all")
    authors = [line.split("\t", 1)[1].strip() for line in out.splitlines() if "\t" in line]
    min_authors = _required_min_authors()
    assert len(authors) >= min_authors, (
        f"{len(authors)} auteur(s) de commits, {min_authors} attendus (un par membre du binôme) : {authors}"
    )


def test_required_min_authors_env_override(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MIN_GIT_AUTHORS", "1")
    assert _required_min_authors() == 1


def test_venv_never_committed(git_root: Path):
    log = _git(git_root, "log", "--all", "--name-only", "--pretty=format:")
    assert ".venv/" not in log, ".venv/ a été commité au moins une fois : nettoyer l'historique ou recommencer le dépôt"
