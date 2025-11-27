# Default port for dev server
PORT ?= 5000
DEBUG_PORT ?= 5001
DB_PATH = instance/app.db

.PHONY: help
help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------
# 🚀 Development and Run
# ---------------------------------------------------------------------

sync:  ## Install project dependencies using uv
	@uv sync

setup:  ## Initialize dev environment (create instance dir, install deps, migrate DB)
	@echo "🔧 Setting up development environment..."
	@uv sync
	@if [ ! -f $(DB_PATH) ]; then \
		echo "🧱 Database not found, running migrations..."; \
		uv run flask db upgrade; \
	else \
		echo "✅ Database already exists: $(DB_PATH)"; \
	fi
	@echo "✅ Setup complete! Run 'make dev'"

dev: ## Run in development mode (with debugger, reload, etc.)
	uv run python3 -m flask run --debug --port=$(DEBUG_PORT)

run: ## Run in production-like mode
	uv run python3 -m flask run --port=$(PORT) --no-debug

routes: ## Show routes
	uv run python3 -m flask routes

shell: ## Launch Flask shell
	uv run python3 -m flask shell

# ---------------------------------------------------------------------
# 🗃️ Database Management
# ---------------------------------------------------------------------
db-init:  ## Initialize migrations directory
	@uv run flask db init

db-migrate:  ## Generate new migration (usage: make db-migrate m="Message")
	@uv run flask db migrate -m "$(m)"

db-upgrade:  ## Apply all migrations
	@uv run flask db upgrade

db-downgrade:  ## Revert last migration
	@uv run flask db downgrade

db-history:  ## Show migration history
	@uv run flask db history

db-current:  ## Show current migration version
	@uv run flask db current

db-heads:  ## Show head revisions (latest migrations)
	@uv run flask db heads

db-show:  ## Show details of a specific revision (usage: make db-show r=<rev>)
	@uv run flask db show $(r)

db-reset:  ## Drop and recreate the database schema (dangerous!)
	@uv run flask db downgrade base
	@uv run flask db upgrade

db-tables: ## Show SQLite DB table list
	@sqlite3 $(DB_PATH) ".tables"

db-status:  ## Show current DB revision and pending migrations
	@echo "=== Database Status ==="
	@CURRENT=$$(uv run flask db current 2>/dev/null | tail -n1); \
	echo "Current DB revision: $$CURRENT"; \
	uv run flask db heads --verbose 2>/dev/null | awk '/Rev:/ && /head/ {getline; print "→ Pending migration(s):"; getline; gsub(/^ +/, ""); print}'

db-schema: ## Show SQLite DB table schema
	@sqlite3 $(DB_PATH) ".schema"

db-shell: ## Open SQLite shell
	@echo "Opening SQLite shell for $(DB_PATH)..."
	@sqlite3 $(DB_PATH)

sqlite: ## Open SQLite shell
	@make db-shell
# ---------------------------------------------------------------------
# 🧪 Tests and Lint
# ---------------------------------------------------------------------

test:
	uv run python -m pytest

code-lint:  ## Lint Python code with Ruff
	@uv run ruff check

code-lint-fix:  ## Auto-fix Python code issues
	@uv run ruff check --fix

template-lint:  ## Lint HTML templates with djlint
	@uv run djlint $$(find app -type f -path "*/templates/*")

template-lint-fix:  ## Auto-fix HTML templates with djlint
	@uv run djlint $$(find app -type f -path "*/templates/*") --reformat

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
