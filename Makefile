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
# 🗃️ Database Management
# ---------------------------------------------------------------------
db-init:
	uv run flask db init

# ---------------------------------------------------------------------
# 🧪 Tests and Lint
# ---------------------------------------------------------------------

test:
	uv run pytest

code-lint:  ## Lint Python code with Ruff
	@uv run ruff check

code-lint-fix:  ## Auto-fix Python code issues
	@uv run ruff check --fix

template-lint:  ## Lint HTML templates with djlint
	@uv run djlint $$(find app -type d -name templates)

template-lint-fix:  ## Auto-fix HTML templates with djlint
	@uv run djlint $$(find app -type d -name templates) --reformat

lint:  ## Run all linters (Ruff + djlint)
	@$(MAKE) code-lint
	@$(MAKE) template-lint

lint-fix:  ## Auto-fix issues in all code and templates
	@$(MAKE) code-lint-fix
	@$(MAKE) template-lint-fix

format:  ## Format Python code with Ruff
	@uv run ruff format

qa:  ## Run all quality checks (lint + tests)
	@$(MAKE) lint
	@$(MAKE) test

fix:  ## Fix and format everything
	@$(MAKE) lint-fix
	@$(MAKE) format
