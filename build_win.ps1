$VenvLocation = pipenv --venv
Write-Host "Using venv location: $VenvLocation" -ForegroundColor DarkGreen

Push-Location src
Write-Host "Cleaning build artefacts ..." -ForegroundColor DarkGreen
Remove-Item -Recurse -Force build
Remove-Item -Recurse -Force dist
Write-Host "Building executable ..."
pipenv run python -m PyInstaller app.spec
Pop-Location

$DistDirectory = "src\dist\PyTimeTrack\"
Write-Host "Copying config.toml" -ForegroundColor DarkGreen
Copy-Item -Path "config.toml" -Destination $DistDirectory

Write-Host "Creating empty report directory" -ForegroundColor DarkGreen
New-Item -Path $DistDirectory -Name "reports" -ItemType "directory" | Out-Null