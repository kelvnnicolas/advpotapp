param([switch]$SQLite)
. "$PSScriptRoot/env.ps1"
Push-Location $projectRoot
try {
    $testSettings = if ($SQLite) { 'config.test_settings' } else { 'config.test_postgres' }
    & .venv/Scripts/python.exe src/manage.py test tests "--settings=$testSettings" --verbosity 1
    if ($LASTEXITCODE -ne 0) { throw 'Testes falharam.' }
    & .venv/Scripts/python.exe src/manage.py makemigrations --check --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'Migrações pendentes.' }
    & .venv/Scripts/python.exe src/manage.py check
    if ($LASTEXITCODE -ne 0) { throw 'Verificação Django falhou.' }
} finally {
    Pop-Location
}
