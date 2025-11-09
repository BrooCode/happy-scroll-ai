# HappyScroll API - PowerShell Helper Script
# Usage: .\run.ps1 <command>
# Example: .\run.ps1 dev

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "HappyScroll Moderation API - Available Commands:" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 install      - Install dependencies" -ForegroundColor Green
    Write-Host "  .\run.ps1 run          - Run the application" -ForegroundColor Green
    Write-Host "  .\run.ps1 dev          - Run in development mode with auto-reload" -ForegroundColor Green
    Write-Host "  .\run.ps1 test         - Run tests" -ForegroundColor Green
    Write-Host "  .\run.ps1 format       - Format code with black" -ForegroundColor Green
    Write-Host "  .\run.ps1 lint         - Lint code with flake8" -ForegroundColor Green
    Write-Host "  .\run.ps1 clean        - Remove cache and temporary files" -ForegroundColor Green
    Write-Host "  .\run.ps1 docker-build - Build Docker image" -ForegroundColor Green
    Write-Host "  .\run.ps1 docker-run   - Run Docker container" -ForegroundColor Green
}

switch ($Command) {
    "install" {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
    "run" {
        Write-Host "Starting application..." -ForegroundColor Yellow
        uvicorn app.main:app --host 0.0.0.0 --port 8000
    }
    "dev" {
        Write-Host "Starting application in development mode..." -ForegroundColor Yellow
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    }
    "test" {
        Write-Host "Running tests..." -ForegroundColor Yellow
        pytest tests/ -v
    }
    "format" {
        Write-Host "Formatting code..." -ForegroundColor Yellow
        black app/ tests/
    }
    "lint" {
        Write-Host "Linting code..." -ForegroundColor Yellow
        flake8 app/ tests/ --max-line-length=100
    }
    "clean" {
        Write-Host "Cleaning cache and temporary files..." -ForegroundColor Yellow
        Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
        Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
        Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force
        Get-ChildItem -Recurse -Filter "*.log" | Remove-Item -Force
        if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }
        if (Test-Path "htmlcov") { Remove-Item -Recurse -Force "htmlcov" }
        if (Test-Path ".coverage") { Remove-Item -Force ".coverage" }
        Write-Host "Clean complete!" -ForegroundColor Green
    }
    "docker-build" {
        Write-Host "Building Docker image..." -ForegroundColor Yellow
        docker build -t happyscroll-api:latest .
    }
    "docker-run" {
        Write-Host "Running Docker container..." -ForegroundColor Yellow
        docker run -p 8000:8000 --env-file .env happyscroll-api:latest
    }
    default {
        Show-Help
    }
}
