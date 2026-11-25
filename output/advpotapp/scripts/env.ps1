$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $projectRoot '.env'
if (-not (Test-Path -LiteralPath $envFile)) {
    throw 'Execute .venv/Scripts/python.exe scripts/init_local.py antes de continuar.'
}
foreach ($line in Get-Content -LiteralPath $envFile) {
    if ($line -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
$env:PYTHONPATH = "$projectRoot;$projectRoot/src"
