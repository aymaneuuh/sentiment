$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$venvPython = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Environnement absent. Lancez d'abord .\installer.ps1."
}

$model = Join-Path $Root "models\sentiment.joblib"
if (-not (Test-Path $model)) {
    throw "Modèle absent. Lancez d'abord .\installer.ps1."
}

Write-Host "Démarrage de l'API sur http://localhost:8000/docs..."
Start-Process -FilePath $venvPython `
    -ArgumentList @("-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000") `
    -WorkingDirectory $Root

Write-Host "Démarrage de Streamlit sur http://localhost:8501..."
Start-Process -FilePath $venvPython `
    -ArgumentList @("-m", "streamlit", "run", "ui/app.py", "--server.headless", "true", "--server.port", "8501") `
    -WorkingDirectory $Root

Start-Sleep -Seconds 4
Start-Process "http://localhost:8501"
