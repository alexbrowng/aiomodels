#!make
.PHONY: tests
tests:
	@uv run pytest

.PHONY: ruff
ruff:
	@uv run ruff check --select I --fix
	@uv run ruff format

.PHONY: quality
quality: ruff

.PHONY: chat
chat:
	@uv run --env-file=".env" chat --model="$(model)"
