Write-Output "Cleaning build artefacts"
$VenvLocation = pipenv --venv
Write-Output "Using venv location: $VenvLocation"
Push-Location ./src
Remove-Item -Recurse -Force build
Remove-Item -Recurse -Force dist
pipenv run python -m PyInstaller app.spec
Pop-Location