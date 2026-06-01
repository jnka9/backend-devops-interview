# Backend DevOps Interview

Servicio de contenido con usuarios, posts, comentarios y tags.

Stack final:

- Django 5 + Django Ninja
- PostgreSQL
- Docker / Docker Compose
- Fly.io para despliegue
- GitHub Actions para CI, CodeQL y deploy

## Setup local

Crear el archivo de entorno:

```sh
cp .env.example .env
```

Levantar app + Postgres con Docker:

```sh
docker compose up --build
```

La API queda disponible en:

```text
http://localhost:8000/api/docs
```

## Comandos Make

```sh
make setup      # crea .env si falta e instala dependencias con uv
make up         # levanta Docker Compose
make down       # detiene Docker Compose
make migrate    # ejecuta migraciones en Docker
make seed       # carga el dataset grande
make test       # corre pytest local con uv
make lint       # corre ruff local con uv
make run        # corre runserver local
make shell      # abre Django shell en Docker
```

## Comandos Docker utiles

Migraciones:

```sh
docker compose run --rm app uv run --no-sync python manage.py migrate
```

Seed grande:

```sh
docker compose run --rm app uv run --no-sync python manage.py seed
```

Tests y lint:

```sh
docker compose run --rm app uv run pytest
docker compose run --rm app uv run ruff check .
```

Vaciar la base conectada por `.env`:

```sh
docker compose run --rm app uv run --no-sync python manage.py flush --noinput
```


## Dataset

El comando `seed` carga aproximadamente:

```text
1000 usuarios
50 tags
100000 posts
500000 comentarios
```

En una base remota puede tardar varios minutos. No se ejecuta automaticamente en cada deploy; las migraciones si se ejecutan como release command de Fly.

## API final

Todas las rutas de negocio viven bajo `/api`.

| Method | Path | Descripcion |
| ------ | ---- | ----------- |
| GET | `/healthz` | Health check |
| GET | `/api/docs` | Documentacion interactiva |
| GET | `/api/posts?limit=50&offset=0` | Posts publicados, newest first |
| GET | `/api/posts/search?q=django&limit=50&offset=0` | Busqueda por titulo/body |
| GET | `/api/posts/by-tag/{slug}?limit=50&offset=0` | Posts por tag |
| GET | `/api/posts/{post_id}` | Detalle de post sin comentarios anidados |
| GET | `/api/posts/{post_id}/comments?limit=50&offset=0` | Comentarios paginados del post |
| POST | `/api/posts` | Crear post |
| POST | `/api/posts/{post_id}/comments` | Crear comentario |
| GET | `/api/users/{user_id}` | Detalle de usuario con contadores |
| GET | `/api/users/find?email=demo@example.com` | Buscar usuario por email |

Ejemplos:

```sh
curl http://localhost:8000/healthz
curl "http://localhost:8000/api/posts?limit=5"
curl "http://localhost:8000/api/posts/search?q=django&limit=5"
curl "http://localhost:8000/api/posts/by-tag/django?limit=5"
curl "http://localhost:8000/api/posts/1"
curl "http://localhost:8000/api/posts/1/comments?limit=5"
```

## Despliegue en Fly.io

Secrets requeridos:

```sh
fly secrets set SECRET_KEY="..."
fly secrets set DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/DB?sslmode=require"
```

Deploy manual:

```sh
fly deploy
```

El deploy ejecuta migraciones:

```toml
release_command = "uv run --no-sync python manage.py migrate"
```

Para cargar el seed en la base remota:

```sh
fly ssh console -a backend-devops-interview -C "uv run --no-sync python manage.py seed"
```

## Validacion realizada

```sh
docker compose build
docker compose run --rm app uv run --no-sync python manage.py migrate
docker compose run --rm app uv run pytest
docker compose run --rm app uv run ruff check .
```

Tambien se probaron por HTTP los endpoints principales, incluyendo posts, comentarios, usuarios y health check.
