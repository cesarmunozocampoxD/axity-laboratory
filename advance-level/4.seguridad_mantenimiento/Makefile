# =============================================================================
# Makefile — common lab tasks
# On Windows without make: run the commands on the right-hand side directly
#   in PowerShell, e.g.:  poetry run pip-audit
# =============================================================================

.PHONY: install test audit-pip audit-safety audit docker-build docker-run

## Install all dependencies (including dev)
install:
	poetry install

## Run the test suite
test:
	poetry run pytest tests/ -v

## Scan for known CVEs in installed packages (pip-audit)
audit-pip:
	poetry run pip-audit

## Scan for known CVEs using Safety (requires free account: safety auth login)
## First-time setup: poetry run safety auth register
audit-safety:
	poetry run safety scan

## Run both audits in sequence
audit: audit-pip audit-safety

## Build the hardened container image
docker-build:
	docker build -t seguridad-mantenimiento:latest .

## Run the container (pass secrets via -e, never bake them in)
docker-run:
	docker run --rm \
		-e API_KEY=replace-with-real-key \
		-e DATABASE_URL=sqlite:////app/app.db \
		seguridad-mantenimiento:latest

## Verify the container runs as a non-root user (should print UID != 0)
docker-whoami:
	docker run --rm --entrypoint id seguridad-mantenimiento:latest
