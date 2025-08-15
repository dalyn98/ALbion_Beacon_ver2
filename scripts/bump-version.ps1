param(
  [Parameter(Mandatory=$true)][string]$NewVersion
)
if (-Not ($NewVersion -match '^v\d+\.\d+\.\d+$')) { Write-Error 'Use semver like v0.6.0'; exit 1 }
Set-Content -Encoding utf8 VERSION $NewVersion
(Get-Content -Raw CHANGELOG.md) -replace '## \[v[0-9.]+\]', "## [$NewVersion]" | Set-Content -Encoding utf8 CHANGELOG.md
git add VERSION CHANGELOG.md
git commit -m "chore(release): bump $NewVersion"
