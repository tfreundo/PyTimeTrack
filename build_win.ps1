param(
    [string]$version = "0.0.0"
)

$win_version_filename = "win_version_info.txt"
Write-Host "Building PyTimeTrack v.$version" -ForegroundColor DarkGreen

Push-Location src

Write-Host "Updating $win_version_filename ..." -ForegroundColor DarkGreen
$version_split = $version.Split(".")
$version_major = $version_split[0]
$version_minor = $version_split[1]
$version_patch = $version_split[2]
(Get-Content $win_version_filename) -replace "filevers=\(\d, \d, \d, \d\)", "filevers=($version_major, $version_minor, $version_patch, 0)" | Set-Content $win_version_filename
(Get-Content $win_version_filename) -replace "prodvers=\(\d, \d, \d, \d\)", "prodvers=($version_major, $version_minor, $version_patch, 0)" | Set-Content $win_version_filename
(Get-Content $win_version_filename) -replace "StringStruct\('FileVersion', '.*'\)", "StringStruct('FileVersion', '$version.0')" | Set-Content $win_version_filename
(Get-Content $win_version_filename) -replace "StringStruct\('ProductVersion', '.*'\)", "StringStruct('ProductVersion', '$version.0')" | Set-Content $win_version_filename


$VenvLocation = pipenv --venv
Write-Host "Using venv location: $VenvLocation" -ForegroundColor DarkGreen

Write-Host "Cleaning build artefacts ..." -ForegroundColor DarkGreen
Remove-Item -Recurse -Force build
Remove-Item -Recurse -Force dist
Write-Host "Building executable ..."  -ForegroundColor DarkGreen
pipenv run python -m PyInstaller app.spec
Pop-Location

$DistDirectory = "src\dist\PyTimeTrack\"
Write-Host "Copying config.toml" -ForegroundColor DarkGreen
Copy-Item -Path "config.toml" -Destination $DistDirectory

Write-Host "Creating empty report directory" -ForegroundColor DarkGreen
New-Item -Path $DistDirectory -Name "reports" -ItemType "directory" | Out-Null

Write-Host "Copying README.md" -ForegroundColor DarkGreen
Copy-Item -Path "README.md" -Destination $DistDirectory