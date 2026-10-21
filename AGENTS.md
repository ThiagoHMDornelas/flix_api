# AGENTS.md — flix_api

> Gerado automaticamente na clonagem para a VPS (21/10/2026). **Revisar**: ajuste o que não bater com a realidade do projeto.

## Visão geral
**API REST** de catálogo de filmes (Django + DRF) com autenticação JWT e schema OpenAPI; serve de backend para o projeto `flix_app`.

**Stack:** Django 5.2.7 · DRF 3.16 · SimpleJWT · drf-spectacular · python-dotenv · Python 3.12 · Docker

## Contexto em camadas
`~/.hermes/SOUL.md` (regras globais) → `~/projetos/python/AGENTS.md` (regras da linguagem) → este arquivo (particularidades do projeto).
Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Estrutura
- `app/` — projeto Django (`app/settings.py`)
- `authentication/` — login JWT
- `genres/`, `actors/`, `movies/`, `reviews/` — domínio do catálogo
- `actors.csv` — carga inicial de atores

## Como rodar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements_dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Testes e lint
```bash
python manage.py test
flake8
```

## Particularidades
- Consumido pelo `flix_app` (Streamlit) — mudanças de contrato/rota quebram o frontend.
- Autenticação por JWT (`rest_framework_simplejwt`); endpoints só aparecem no schema do drf-spectacular se estiverem anotados.

## Convenções
- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
