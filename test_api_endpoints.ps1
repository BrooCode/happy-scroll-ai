# HappyScroll API Testing Script
# Tests the moderation endpoint with various safe images

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HappyScroll API - Moderation Test Suite" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"

# Check if server is running
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/api/health" -ErrorAction Stop
    Write-Host "✅ Server is running: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Server is not running. Please start it with:" -ForegroundColor Red
    Write-Host "   python -m uvicorn app.main:app --reload`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n" + "="*50

# Test cases with safe, publicly available images
$testCases = @(
    @{
        name = "Test 1: Safe Nature Image"
        description = "Google official image - should be very safe"
        url = "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Dove_2880p_001.width-1300.jpg"
        expectedSafe = $true
    },
    @{
        name = "Test 2: YouTube Music Video (Rick Astley)"
        description = "Popular safe music video thumbnail"
        url = "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
        expectedSafe = $true
    },
    @{
        name = "Test 3: YouTube Kids Content"
        description = "Educational kids content"
        url = "https://i.ytimg.com/vi/9bZkp7q19f0/maxresdefault.jpg"
        expectedSafe = $true
    },
    @{
        name = "Test 4: Google Cloud Sample Image"
        description = "Official Google Cloud Vision sample"
        url = "https://storage.googleapis.com/cloud-samples-data/vision/demo-img.jpg"
        expectedSafe = $true
    },
    @{
        name = "Test 5: Product Image"
        description = "Safe product photography"
        url = "https://storage.googleapis.com/cloud-samples-data/vision/label/wakeupcat.jpg"
        expectedSafe = $true
    }
)

$passedTests = 0
$failedTests = 0

foreach ($test in $testCases) {
    Write-Host "`n$($test.name)" -ForegroundColor Yellow
    Write-Host "Description: $($test.description)" -ForegroundColor Gray
    Write-Host "URL: $($test.url)" -ForegroundColor Gray
    Write-Host "Testing..." -NoNewline
    
    try {
        $body = @{ image_url = $test.url } | ConvertTo-Json
        $result = Invoke-RestMethod -Uri "$baseUrl/api/moderate" `
            -Method Post `
            -ContentType "application/json" `
            -Body $body `
            -ErrorAction Stop
        
        Write-Host " Done" -ForegroundColor Green
        
        # Display results
        Write-Host "`nResults:" -ForegroundColor Cyan
        Write-Host "  Allowed: $($result.allowed)" -ForegroundColor $(if ($result.allowed) { "Green" } else { "Red" })
        Write-Host "  Safe: $($result.safe)" -ForegroundColor $(if ($result.safe) { "Green" } else { "Red" })
        Write-Host "  Service: $($result.service)"
        Write-Host "  Threshold: $($result.threshold)"
        
        Write-Host "`n  Categories:" -ForegroundColor Cyan
        foreach ($category in $result.categories.PSObject.Properties) {
            $icon = if ($category.Value) { "⚠️" } else { "✅" }
            $color = if ($category.Value) { "Yellow" } else { "Green" }
            Write-Host "    $icon $($category.Name): $($category.Value)" -ForegroundColor $color
        }
        
        Write-Host "`n  Likelihood Scores:" -ForegroundColor Cyan
        foreach ($score in $result.likelihood_scores.PSObject.Properties) {
            $icon = switch ($score.Value) {
                "VERY_UNLIKELY" { "✅" }
                "UNLIKELY" { "✅" }
                "POSSIBLE" { "⚠️" }
                "LIKELY" { "❌" }
                "VERY_LIKELY" { "❌" }
                default { "❓" }
            }
            Write-Host "    $icon $($score.Name): $($score.Value)"
        }
        
        # Check if result matches expectation
        if ($result.safe -eq $test.expectedSafe) {
            Write-Host "`n✅ TEST PASSED" -ForegroundColor Green
            $passedTests++
        } else {
            Write-Host "`n❌ TEST FAILED: Expected safe=$($test.expectedSafe), got safe=$($result.safe)" -ForegroundColor Red
            $failedTests++
        }
        
    } catch {
        Write-Host " Failed" -ForegroundColor Red
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        $failedTests++
    }
    
    Write-Host ("-"*50)
}

# Summary
Write-Host "`n" + "="*50
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "="*50
Write-Host "Total Tests: $($testCases.Count)"
Write-Host "Passed: $passedTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor $(if ($failedTests -gt 0) { "Red" } else { "Green" })

if ($failedTests -eq 0) {
    Write-Host "`n🎉 All tests passed! Your API is working correctly." -ForegroundColor Green
} else {
    Write-Host "`n⚠️ Some tests failed. Please check the output above." -ForegroundColor Yellow
}

Write-Host "`n" + "="*50

# Additional info
Write-Host "`nℹ️ Notes:" -ForegroundColor Cyan
Write-Host "  - All test images are safe, publicly available images"
Write-Host "  - To adjust sensitivity, change SAFETY_THRESHOLD in .env file"
Write-Host "  - Current threshold: POSSIBLE (recommended for kids)"
Write-Host "  - API Documentation: http://localhost:8000/docs"
Write-Host "`n"
