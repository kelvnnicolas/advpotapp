"""Generate local secrets; never print them or overwrite an existing environment."""
from pathlib import Path
import secrets

root = Path(__file__).resolve().parent.parent
target = root / '.env'
if target.exists():
    print('Configuração local existente preservada.')
else:
    content = '\n'.join([
        'ADVPOT_ENV=local',
        f'ADVPOT_SECRET_KEY={secrets.token_urlsafe(50)}',
        'ADVPOT_ALLOWED_HOSTS=localhost,127.0.0.1',
        'POSTGRES_DB=advpot', 'POSTGRES_USER=advpot',
        f'POSTGRES_PASSWORD={secrets.token_urlsafe(40)}',
        'POSTGRES_HOST=127.0.0.1', 'POSTGRES_PORT=55432', '',
    ])
    with target.open('x', encoding='utf-8') as file:
        file.write(content)
    print('Configuração local gerada em .env; segredos não exibidos.')
