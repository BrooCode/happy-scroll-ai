# Quick Setup Script for HappyScroll API
# Run this script to set up your development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HappyScroll API - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check .env file
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Remember to update your OPENAI_API_KEY in .env file!" -ForegroundColor Yellow
} else {
    Write-Host "✗ .env file not found" -ForegroundColor Red
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY!" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your OpenAI API key" -ForegroundColor White
Write-Host "2. Run: .\run.ps1 dev" -ForegroundColor White
Write-Host "3. Open: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  .\run.ps1 dev   - Start development server" -ForegroundColor White
Write-Host "  .\run.ps1 test  - Run tests" -ForegroundColor White
Write-Host "  .\run.ps1 help  - Show all commands" -ForegroundColor White
Write-Host ""
