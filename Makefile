.PHONY: setup up down migrate seed test lint run shell

setup:
	cp -n .env.example .env || true
	uv sync --dev

up:
	docker compose up --build

down:
	docker compose down

migrate:
	docker compose run --rm app uv run python manage.py migrate

seed:
	docker compose run --rm app uv run python manage.py seed

test:
	uv run pytest

lint:
	uv run ruff check .

run:
	uv run python manage.py runserver

shell:
	docker compose run --rm app uv run python manage.py shell
