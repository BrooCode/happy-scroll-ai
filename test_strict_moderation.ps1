# Test Script for Strict Content Moderation
# This script tests YouTube video analysis with strict Indian parenting norms

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Strict Content Moderation Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Wait for server to be ready
Write-Host "Waiting for server to reload..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test video URL
$testUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

Write-Host "Testing with video: $testUrl" -ForegroundColor Yellow
Write-Host ""

try {
    # Make API request
    $body = @{
        video_url = $testUrl
    } | ConvertTo-Json
    
    Write-Host "Sending request..." -ForegroundColor Gray
    $result = Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -TimeoutSec 120
    
    # Display results
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ ANALYSIS COMPLETE" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "�️ Safety Analysis Result:" -ForegroundColor Cyan
    Write-Host ""
    
    if ($result.is_safe) {
        Write-Host "  Status: ✅ SAFE FOR CHILDREN" -ForegroundColor Green
    } else {
        Write-Host "  Status: ❌ NOT SAFE FOR CHILDREN" -ForegroundColor Red
    }
    Write-Host ""
    
    Write-Host "  Gemini Verdict: $($result.gemini_verdict)" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "  Reason:" -ForegroundColor White
    Write-Host "  $($result.reason)" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Test Completed Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
} catch {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ ERROR" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    
    if ($_.Exception.Message -match "gemini") {
        Write-Host "💡 Tip: Check your Gemini API key in .env file" -ForegroundColor Yellow
        Write-Host "   Make sure you're using: gemini-2.0-flash" -ForegroundColor Yellow
    }
    
    if ($_.Exception.Message -match "Connection refused") {
        Write-Host "💡 Tip: Make sure the server is running:" -ForegroundColor Yellow
        Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
