.PHONY: run install test clean docker-build docker-up docker-down fix-lint

# Include environment variables from .env-local
include .env-local
export

PYTHONPATH := $(PYTHONPATH):$(CURDIR)/file_api_app

# Install dependencies
install:
	python -m pip install -e ".[dev]"

# Run the application
run:
	python -m file_api_app

# Run tests
test:
	pytest

# Format code with ruff
fix-lint:
	ruff format .

# Docker commands
docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down