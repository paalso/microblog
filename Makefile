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
