install:
	uv sync

run:
	uv run flask run

dev:
	uv run flask --debug run
