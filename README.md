# Flix API

![Testes](https://github.com/ThiagoHMDornelas/flix_api/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-5.2-092E20)
![License](https://img.shields.io/badge/license-MIT-green)

API REST para gerenciamento de filmes, desenvolvida com Django e Django REST Framework. Serve como backend do sistema, oferecendo endpoints para cadastro e consulta de filmes, gêneros, atores/atrizes e avaliações, com autenticação via JWT e controle de permissões.

## Sumário

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Executar com Docker](#executar-com-docker)
- [Testes](#testes)
- [Autenticação com JWT](#autenticação-com-jwt)
- [Principais rotas](#principais-rotas)
- [Documentação da API](#documentação-da-api)
- [Detalhes das funcionalidades](#detalhes-das-funcionalidades)
- [Permissões](#permissões)
- [Importação de atores via CSV](#importação-de-atores-via-csv)
- [Painel administrativo](#painel-administrativo)
- [Relação com o Flix App](#relação-com-o-flix-app)
- [Licença](#licença)

## Visão geral

O **Flix API** é o backend do sistema de catálogo de filmes. Ele expõe uma API REST versionada em `/api/v1/`, persiste os dados em SQLite e protege os endpoints com autenticação JWT e permissões baseadas no modelo do Django.

## Funcionalidades

- Autenticação com JWT (obtenção, renovação e verificação de token)
- CRUD de gêneros
- CRUD de atores e atrizes
- CRUD de filmes (com relacionamento N:N com atores)
- CRUD de avaliações (com nota de 0 a 5 estrelas)
- Estatísticas agregadas dos filmes
- Permissões por usuário, vinculadas às permissões do modelo no Django
- Comando de gerenciamento para importar atores a partir de CSV

## Tecnologias

- Python
- Django 5.2
- Django REST Framework
- Simple JWT
- drf-spectacular (documentação Swagger/OpenAPI)
- SQLite
- Docker e Docker Compose
- GitHub Actions (CI)
- flake8 (desenvolvimento)

## Estrutura do projeto

```
flix-api/
├── app/                  # configurações do projeto (settings, urls, permissions)
├── authentication/       # rotas de autenticação JWT
├── genres/               # app de gêneros
├── actors/               # app de atores/atrizes (+ comando import_actors)
├── movies/               # app de filmes (+ endpoint de estatísticas)
├── reviews/              # app de avaliações
├── .github/workflows/    # pipeline de CI (GitHub Actions)
├── Dockerfile
├── docker-compose.yml
├── .env.example          # exemplo de variáveis de ambiente
├── actors.csv            # exemplo de arquivo para importação
├── manage.py
├── requirements.txt
└── requirements_dev.txt
```

## Instalação e execução

Pré-requisitos:

- Python 3.10 ou superior instalado

Acesse a pasta do projeto:

    cd flix_api

Crie um ambiente virtual:

    python -m venv .venv

No Windows, ative o ambiente virtual:

    .venv\Scripts\activate

No Linux ou macOS, ative o ambiente virtual:

    source .venv/bin/activate

Instale as dependências:

    pip install -r requirements.txt

Opcionalmente, para desenvolvimento (lint), instale também:

    pip install -r requirements_dev.txt

Execute as migrações:

    python manage.py migrate

Crie um usuário administrador:

    python manage.py createsuperuser

Inicie o servidor:

    python manage.py runserver

A documentação da API estará disponível em:

    http://127.0.0.1:8000/api/docs/

## Variáveis de ambiente

As configurações sensíveis são lidas de variáveis de ambiente, com valores padrão para desenvolvimento. O projeto usa o pacote `python-dotenv` para carregar um arquivo `.env` na raiz.

1. Copie o arquivo de exemplo:

    No Windows:

        copy .env.example .env

    No Linux ou macOS:

        cp .env.example .env

2. Ajuste os valores conforme necessário.

Variáveis disponíveis:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `SECRET_KEY` | Chave secreta do Django | chave insegura de desenvolvimento |
| `DEBUG` | Modo de depuração (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula | `*` |

O arquivo `.env` não é versionado (está no `.gitignore`).

## Executar com Docker

A forma recomendada de rodar a API. O Docker Compose sobe o serviço já configurado (Django + DRF + SQLite), sem precisar montar o ambiente Python manualmente.

**Pré-requisitos:**

- Docker Desktop instalado e em execução (engine)
- Docker Compose (já vem com o Docker Desktop)
- Git instalado (para clonar o repositório)
- A porta `8000` livre

> **Importante:** o Docker Desktop sozinho **não** faz o setup inicial — ele é o *engine* e o painel de gerenciamento. Clonar o repositório e rodar `docker compose up --build` são feitos pelo **terminal**; o Docker Desktop é ótimo para acompanhar logs, iniciar/parar e abrir um terminal dentro do container **depois** que a stack subiu.

> O Docker **não** precisa do arquivo `.env`: as variáveis já vêm definidas no `docker-compose.yml`. O `.env.example` é usado apenas na execução local (fora do Docker).

### Passo a passo (via shell / PowerShell)

**1. Clone o repositório**

```powershell
git clone https://github.com/ThiagoHMDornelas/flix_api.git
cd flix_api
```

> O `git clone` cria a pasta `flix_api` dentro da pasta atual, e o `cd` entra nela. Se você **já está dentro** da pasta do projeto, **pule o `cd`**.

**2. Suba a stack.** Na primeira execução o Docker compila a imagem do projeto — pode levar alguns minutos:

```powershell
docker compose up --build -d
```

**3. Confira os containers:**

```powershell
docker compose ps
```

Espere o serviço `web` como `Up`.

| Serviço | Porta | Acesso |
|---|---|---|
| `web` | 8000 | `http://localhost:8000` |

**4. Acesse a API:**

- Documentação Swagger: `http://localhost:8000/api/docs/`
- Schema OpenAPI: `http://localhost:8000/api/schema/`
- Painel administrativo: `http://localhost:8000/admin/`

Os endpoints ficam sob o prefixo `http://localhost:8000/api/v1/`.

As migrações são aplicadas automaticamente na inicialização.

**5. Crie o usuário administrador:**

```powershell
docker compose exec web python manage.py createsuperuser
```

**6. Comandos úteis:**

```powershell
docker compose logs -f web     # logs da API
docker compose restart web     # reinicia a API
docker compose down            # para e remove os containers
```

> O banco SQLite é criado dentro do container, então os dados **não persistem** após um `docker compose down`.

### Usando o Docker Desktop (interface gráfica)

Depois que a stack estiver no ar (passo 2), o Docker Desktop ajuda a operar. Na aba **Containers** você verá o serviço `web`:

- **Logs**: clique no container → aba *Logs* (equivale a `docker compose logs`).
- **Start / Stop / Restart**: botões no topo do container.
- **Terminal no container**: botão *Exec* (útil para depurar dentro do container).
- **Abrir no navegador**: clique na porta publicada (`8000:8000`).

O que **não** dá para fazer pela interface gráfica: clonar o repositório e rodar `docker compose up --build` em um clone novo (isso é feito pelo terminal).

### Problemas comuns

- **A API não responde**
  - Veja os logs: `docker compose logs -f web`
  - Confirme que o container está `Up`: `docker compose ps`
- **Erro de porta em uso** (`8000`) → pare o serviço que ocupa a porta ou ajuste o mapeamento no `docker-compose.yml` (ex.: `8001:8000`) e acesse em `http://localhost:8001`
- **Os dados sumiram após reiniciar** → é esperado: o SQLite fica dentro do container e não persiste após um `docker compose down`

## Testes

A suíte de testes cobre models, endpoints, validações, exigência de autenticação e os cálculos agregados. Execute:

    python manage.py test

Para executar apenas os testes de um app:

    python manage.py test movies

Os testes utilizam um banco de dados separado, criado e destruído automaticamente, sem afetar o `db.sqlite3`.

A suíte também roda automaticamente a cada `push` e `pull request` via **GitHub Actions** (`.github/workflows/tests.yml`), e o resultado é exibido no badge no topo deste README.

## Autenticação com JWT

Para obter os tokens, envie usuário e senha para:

    POST /api/v1/authentication/token/

Exemplo de dados enviados:

    {
        "username": "seu_usuario",
        "password": "sua_senha"
    }

A resposta retorna os tokens `access` e `refresh`:

    {
        "access": "eyJ...",
        "refresh": "eyJ..."
    }

Nas requisições protegidas, envie o token de acesso no cabeçalho:

    Authorization: Bearer seu_access_token

Configurações de tempo de vida dos tokens (`app/settings.py`):

- **Access token:** 5 minutos
- **Refresh token:** 1 dia

Para renovar o token de acesso, use o `refresh` em `POST /api/v1/authentication/token/refresh/`.

## Principais rotas

A API utiliza o prefixo `/api/v1/`.

### Autenticação

    POST /api/v1/authentication/token/
    POST /api/v1/authentication/token/refresh/
    POST /api/v1/authentication/token/verify/

### Filmes

    GET    /api/v1/movies/
    POST   /api/v1/movies/
    GET    /api/v1/movies/<id>
    PUT    /api/v1/movies/<id>
    PATCH  /api/v1/movies/<id>
    DELETE /api/v1/movies/<id>
    GET    /api/v1/movies/stats/

### Gêneros

    GET    /api/v1/genres/
    POST   /api/v1/genres/
    GET    /api/v1/genres/<id>/
    PUT    /api/v1/genres/<id>/
    PATCH  /api/v1/genres/<id>/
    DELETE /api/v1/genres/<id>/

### Atores

    GET    /api/v1/actors/
    POST   /api/v1/actors/
    GET    /api/v1/actors/<id>/
    PUT    /api/v1/actors/<id>/
    PATCH  /api/v1/actors/<id>/
    DELETE /api/v1/actors/<id>/

### Avaliações

    GET    /api/v1/reviews/
    POST   /api/v1/reviews/
    GET    /api/v1/reviews/<id>
    PUT    /api/v1/reviews/<id>
    PATCH  /api/v1/reviews/<id>
    DELETE /api/v1/reviews/<id>

## Documentação da API

A API possui documentação interativa gerada automaticamente com `drf-spectacular`:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **Schema OpenAPI:** http://127.0.0.1:8000/api/schema/

O schema também pode ser exportado para arquivo, útil para ferramentas de integração:

    python manage.py spectacular --file schema.yml

## Detalhes das funcionalidades

### Filmes

- **`GET /api/v1/movies/`** e **`GET /api/v1/movies/<id>`** retornam os dados com o gênero e os atores expandidos (objetos completos) e um campo calculado `rate` (média das avaliações, arredondada em 1 casa decimal).
- Nas operações de escrita, os campos `genre` e `actors` são enviados apenas com seus identificadores (IDs).
- Validações aplicadas no cadastro/edição:
  - `release_date` (data de lançamento) não pode ser anterior a **1990**;
  - `resume` (resumo) não pode ultrapassar **200 caracteres**.

Exemplo de payload de criação:

    {
        "title": "Oppenheimer",
        "genre": 1,
        "release_date": "2023-07-21",
        "actors": [1, 2],
        "resume": "A história do físico J. Robert Oppenheimer..."
    }

### Estatísticas de filmes

**`GET /api/v1/movies/stats/`** retorna dados agregados do catálogo:

    {
        "movies_total": 10,
        "movies_by_genre": [
            { "genre__name": "Drama", "count": 4 },
            { "genre__name": "Ação", "count": 6 }
        ],
        "reviews_total": 25,
        "average_stars": 4.2
    }

- `movies_total`: total de filmes cadastrados;
- `movies_by_genre`: quantidade de filmes agrupada por gênero;
- `reviews_total`: total de avaliações;
- `average_stars`: média geral das estrelas (0 quando não houver avaliações).

### Gêneros

- Modelo `Genre` com o campo `name` (obrigatório).
- CRUD completo via API.

### Atores

- Modelo `Actor` com `name`, `birthday` (opcional) e `nationality` (opcional).
- A nacionalidade é restrita às opções:
  - `USA` — Estados Unidos
  - `BRL` — Brasil
- CRUD completo via API.

### Avaliações

- Modelo `Review` vinculado a um filme, com `stars` e `comment` (opcional).
- A nota `stars` aceita apenas valores entre **0 e 5**.
- Ao excluir um filme com avaliações, a integridade referencial é protegida (`on_delete=PROTECT`).

## Permissões

Além de exigir usuário autenticado (`IsAuthenticated`), cada endpoint aplica a permissão `GlobalPermissionClass` (`app/permissions.py`). Essa classe monta dinamicamente a permissão do Django no formato:

    <app>.<acao>_<modelo>

Por exemplo, para criar um filme (`POST /api/v1/movies/`), o usuário precisa da permissão `movies.add_movie`. A ação é derivada do método HTTP:

| Método | Ação    | Permissão gerada        |
|--------|---------|-------------------------|
| GET    | view    | `app.view_model`        |
| POST   | add     | `app.add_model`         |
| PUT/PATCH | change | `app.change_model`    |
| DELETE | delete  | `app.delete_model`      |

As permissões podem ser atribuídas aos usuários pelo painel administrativo do Django.

## Importação de atores via CSV

O projeto inclui o comando de gerenciamento `import_actors`, que lê um arquivo CSV e cria os atores no banco.

Formato esperado do CSV (colunas: `name`, `birthday`, `nationality`):

    name,birthday,nationality
    Julia Roberts,1967-10-28,USA
    Wagner Moura,1976-06-27,BRL

Execução:

    python manage.py import_actors actors.csv

## Painel administrativo

O painel administrativo pode ser acessado em:

    http://127.0.0.1:8000/admin/

Nele é possível gerenciar usuários, permissões e os registros de gêneros, atores, filmes e avaliações.

## Relação com o Flix App

O **Flix API** funciona como backend do sistema. O **Flix App** (frontend) consome seus endpoints para realizar login, consultar dados e cadastrar informações.

    Flix App (frontend) -> Flix API (backend) -> Banco de dados

O frontend fica em um repositório separado:

> https://github.com/ThiagoHMDornelas/flix_app

Para utilizá-lo, basta iniciar o Flix API e configurar o `BASE_URL` do Flix App para apontar para `http://127.0.0.1:8000/api/v1/`.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
