. "$PSScriptRoot/env.ps1"
Push-Location $projectRoot
try {
    docker compose --project-name advpotapp-m1 --env-file .env -f deploy/compose.local.yml up -d --wait db
    if ($LASTEXITCODE -ne 0) { throw 'PostgreSQL não iniciou.' }
    & .venv/Scripts/python.exe src/manage.py migrate
    if ($LASTEXITCODE -ne 0) { throw 'Migrações não concluídas.' }
    & .venv/Scripts/python.exe src/manage.py runserver 127.0.0.1:8765 --noreload
} finally {
    Pop-Location
}
