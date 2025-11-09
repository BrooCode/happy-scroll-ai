.PHONY: help install run dev test format lint clean docker-build docker-run

# Default target
help:
	@echo "HappyScroll Moderation API - Available Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the application"
	@echo "  make dev          - Run in development mode with auto-reload"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Lint code with flake8"
	@echo "  make clean        - Remove cache and temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

# Install dependencies
install:
	pip install -r requirements.txt

# Run the application
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run in development mode
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	pytest tests/ -v

# Format code
format:
	black app/ tests/

# Lint code
lint:
	flake8 app/ tests/ --max-line-length=100

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Build Docker image
docker-build:
	docker build -t happyscroll-api:latest .

# Run Docker container
docker-run:
	docker run -p 8000:8000 --env-file .env happyscroll-api:latest
