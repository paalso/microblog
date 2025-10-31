# Default port for dev server
PORT ?= 5000

# ---------------------------------------------------------------------
# 🚀 Development and Run
# ---------------------------------------------------------------------

dev:
	uv run python3 -m flask --app microblog run --debug --port=$(PORT)

routes:
	uv run python3 -m flask --app microblog routes

shell:
	uv run python3

# ---------------------------------------------------------------------
# 🧪 Tests and Lint
# ---------------------------------------------------------------------

test:
	uv run pytest

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

check: test lint
