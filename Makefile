# NCC School Management - Makefile
# Utility commands for development and deployment

.PHONY: help install install-dev migrate makemigrations runserver test test-coverage lint format clean docker-build docker-up docker-down

# Default target
help:
	@echo "NCC School Management - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  migrate          Run database migrations"
	@echo "  makemigrations   Create new database migrations"
	@echo "  runserver        Start Django development server"
	@echo "  shell            Start Django shell"
	@echo "  superuser        Create Django superuser"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-coverage    Run tests with coverage report"
	@echo "  test-fast        Run tests without migrations"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run flake8 linter"
	@echo "  format           Format code with black and isort"
	@echo "  format-check     Check code formatting"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build     Build Docker images"
	@echo "  docker-up        Start Docker services"
	@echo "  docker-down      Stop Docker services"
	@echo "  docker-logs      Show Docker logs"
	@echo ""
	@echo "Database:"
	@echo "  db-reset         Reset database (WARNING: destroys data)"
	@echo "  db-backup        Create database backup"
	@echo ""
	@echo "Utilities:"
	@echo "  clean            Clean temporary files"
	@echo "  requirements     Generate requirements.txt"

# Development commands
install:
	uv sync --no-dev

install-dev:
	uv sync

migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

runserver:
	uv run python manage.py runserver

shell:
	uv run python manage.py shell

superuser:
	uv run python manage.py createsuperuser

# Testing commands
test:
	uv run pytest api/tests.py comercial/tests.py common/tests.py crm/tests.py financial/tests.py management/tests.py

test-coverage:
	uv run pytest --cov=. --cov-report=html --cov-report=term-missing api/tests.py comercial/tests.py common/tests.py crm/tests.py financial/tests.py management/tests.py

test-fast:
	uv run pytest --nomigrations api/tests.py comercial/tests.py common/tests.py crm/tests.py financial/tests.py management/tests.py

# Code quality commands
lint:
	uv run flake8 .

format:
	uv run black .
	uv run isort .

format-check:
	uv run black --check .
	uv run isort --check-only .

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Database commands
db-reset:
	@echo "WARNING: This will destroy all data in the database!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	uv run python manage.py flush --noinput
	uv run python manage.py migrate

db-backup:
	@echo "Creating database backup..."
	@mkdir -p backups
	@timestamp=$$(date +%Y%m%d_%H%M%S) && \
	uv run python manage.py dumpdata > backups/backup_$$timestamp.json && \
	echo "Backup created: backups/backup_$$timestamp.json"

# Utility commands
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

requirements:
	uv export --format requirements-txt > requirements.txt
	uv export --format requirements-txt --dev > requirements-dev.txt

# Production commands
collectstatic:
	uv run python manage.py collectstatic --noinput

# Development setup
setup-dev: install-dev migrate
	@echo "Development environment setup complete!"
	@echo "Run 'make runserver' to start the development server"

# CI/CD commands
ci-test: lint test
	@echo "CI tests passed!"

ci-format-check: format-check
	@echo "Code formatting check passed!"
