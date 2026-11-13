$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) {
    throw "Python est introuvable. Installez Python 3.11 ou plus récent, puis relancez ce script."
}

$venvPython = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Création de l'environnement Python..."
    & $pythonCommand.Source -m venv (Join-Path $Root ".venv")
}

Write-Host "Installation des dépendances et du paquet..."
& $venvPython -m pip install -e ".[ui]"

$model = Join-Path $Root "models\sentiment.joblib"
if (-not (Test-Path $model)) {
    Write-Host "Entraînement du modèle de démonstration..."
    & $venvPython "src\train.py"
}

Write-Host ""
Write-Host "Installation terminée. Lancez .\lancer.ps1 pour démarrer l'application."
