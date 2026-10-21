# AGENTS.md — flix-api

API REST de catálogo de filmes (filmes, gêneros, atores, avaliações) com JWT e Swagger, backend do `flix_app` (Streamlit). Django 5.2.7 + DRF 3.16.1 · SimpleJWT 5.5.1 · drf-spectacular 0.30 · python-dotenv · Python 3.12 · SQLite.

## Contexto em camadas
`SOUL.md` (regras globais do agente) → `AGENTS.md` da pasta da linguagem (regras comuns) → este arquivo (particularidades do projeto). Em conflito, vale o mais específico (este arquivo), exceto em regras de segurança/global.

## Arquitetura

- **Pacote de settings**: `app` (`app.settings`), `ROOT_URLCONF = 'app.urls'`.
- **Sem views HTML**: todos os endpoints são DRF e ficam sob `/api/v1/`; docs interativas em `/api/docs/` (Swagger) e schema em `/api/schema/` (`drf_spectacular`).
- **Autenticação**: `JWTAuthentication` global (SimpleJWT). Token endpoints em `/api/v1/authentication/token/`, `/token/refresh/`, `/token/verify/`. Access token **5 minutos**, refresh **1 dia**.
- **Permissões**: toda view usa `IsAuthenticated` + `app.permissions.GlobalPermissionClass`, que mapeia o método HTTP para a permissão padrão do Django (`GET→view`, `POST→add`, `PUT/PATCH→change`, `DELETE→delete`) usando `view.queryset.model` — logo, **toda view obrigatoriamente define `queryset`**.
- **Banco**: apenas SQLite (`db.sqlite3`), sem seleção de backend.
- **Locale**: `pt-BR`, fuso `UTC` (diferente dos projetos irmãos que usam `America/Sao_Paulo`).

### Apps

| App | Finalidade | Observações |
|---|---|---|
| `app/` | Config, URLs raiz, `app.permissions.GlobalPermissionClass` | Roteia `/api/v1/` para todos os apps |
| `authentication/` | Jwt endpoints (TokenObtainPair/Refresh/Verify) | Sem views/models próprios |
| `genres/` | CRUD de gêneros | DRF generics |
| `actors/` | CRUD de atores/atrizes + comando `import_actors` | Importa CSV (`name,birthday,nationality`) via `python manage.py import_actors actors.csv` |
| `movies/` | CRUD de filmes (N:N com atores) | Serializer duplo: `MovieListDetailSerializer` (GET, aninhado + `rate` médio de review) vs `MovieModelSerializer` (POST/PUT) |
| `reviews/` | CRUD de avaliações | Campo `stars`; alimenta o `rate` dos filmes |

## Testes e lint

- Suíte obrigatória antes de entregar: **`python manage.py test`** (runner nativo do Django).
- Lint com flake8 (`.flake8`: ignora E501, exclui `.venv`).
- O CI (`.github/workflows/tests.yml`) roda apenas `python manage.py test` em Python 3.12 a cada push/PR (flake8 não está no CI).

## Variáveis de ambiente

Apenas `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` — carregadas por `python-dotenv` (`load_dotenv(BASE_DIR / '.env')` no settings). Não há chaves de IA nem de banco externo.

## Contratos e integrações

- **Contrato com `flix_app` (Streamlit)**: o frontend consome `/api/v1/` com `BASE_URL = http://127.0.0.1:8000/api/v1/`. Mudar rota, payload ou autenticação quebra o frontend — alterar os dois lados em conjunto.
- **Ambos os projetos são atualizados em par** (versionamento dos serializers em especial).

## Validações e padrões importantes

- `MovieModelSerializer.validate_release_date`: rejeita filmes lançados antes de 1990.
- `Movie.resume`: `MaxLengthValidator(200)` no model (passa a mensagem customizada).
- Views com método GET retornam serializer de listagem/detail e POST/PUT retornam o serializer de escrita (`get_serializer_class` switchear por método é o padrão nos apps).
- A documentação do Swagger é gerada automaticamente; view extra (`MovieStatsView`, `APIView` puro) usa `@extend_schema(responses=...)`.

## Docker

Serviço web único (migra + runserver em `0.0.0.0:8000`); sem serviço de banco no compose, o container usa a secret key de desenvolvimento embutida no compose.

## Convenções

- Secrets **sempre** em `.env` (nunca hardcode); mantenha o `.env.example` atualizado e o `.env` fora do versionamento.
- Migrações que apagam ou tornam campo obrigatório sem `default` precisam de aviso antes de rodar em produção.
- Mensagens de UI/validação em português do Brasil, revisadas (acentuação e concordância).
- Não commitar/pushar por conta própria: as alterações ficam prontas para o usuário revisar e commitar.
- Preservar encoding dos arquivos ao editar (não converter ANSI ↔ UTF-8 sem pedido explícito).
