# Test Video Analysis API
# Quick test script for the video analysis endpoint

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Video Analysis API - Test Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"

# Check if server is running
Write-Host "`nChecking if server is running..." -NoNewline
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/api/health" -ErrorAction Stop
    Write-Host " ✅" -ForegroundColor Green
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "Server is not running. Please start it with:" -ForegroundColor Yellow
    Write-Host "  python -m uvicorn app.main:app --reload`n" -ForegroundColor Yellow
    exit 1
}

# Check video analysis service status
Write-Host "`nChecking video analysis service status..." -NoNewline
try {
    $status = Invoke-RestMethod -Uri "$baseUrl/api/analyze_video/status" -ErrorAction Stop
    
    if ($status.status -eq "ready") {
        Write-Host " ✅" -ForegroundColor Green
        Write-Host "  Speech-to-Text: $($status.components.speech_to_text)" -ForegroundColor Gray
        Write-Host "  Gemini AI: $($status.components.gemini_ai)" -ForegroundColor Gray
        Write-Host "  Project ID: $($status.project_id)" -ForegroundColor Gray
    } else {
        Write-Host " ⚠️" -ForegroundColor Yellow
        Write-Host "  Status: $($status.status)" -ForegroundColor Yellow
        Write-Host "  Message: $($status.message)" -ForegroundColor Yellow
        
        if ($status.status -eq "not_configured") {
            Write-Host "`n❌ Configuration Error:" -ForegroundColor Red
            Write-Host "Please set the following in your .env file:" -ForegroundColor Yellow
            Write-Host "  GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json"
            Write-Host "  GEMINI_API_KEY=your-gemini-api-key"
            Write-Host "`nGet Gemini API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
            exit 1
        }
    }
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n" + "="*50
Write-Host "✅ Video Analysis API is ready!" -ForegroundColor Green
Write-Host "="*50

Write-Host "`n📝 To test the endpoint, you need:" -ForegroundColor Cyan
Write-Host "  1. A video file uploaded to Google Cloud Storage"
Write-Host "  2. The gs:// URL of that video"
Write-Host ""
Write-Host "Example usage:" -ForegroundColor Yellow
Write-Host '  $body = @{ video_url = "gs://my-bucket/video.mp4" } | ConvertTo-Json'
Write-Host '  $result = Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" -Method Post -ContentType "application/json" -Body $body'
Write-Host ""
Write-Host "Interactive documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# Prompt for test
Write-Host "Do you have a video in Google Cloud Storage to test? (y/n): " -NoNewline -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "y") {
    Write-Host "`nEnter your video URL (gs://bucket/video.mp4): " -NoNewline -ForegroundColor Yellow
    $videoUrl = Read-Host
    
    if ($videoUrl -and $videoUrl.StartsWith("gs://")) {
        Write-Host "`nAnalyzing video (this may take a few minutes)..." -ForegroundColor Cyan
        Write-Host "URL: $videoUrl" -ForegroundColor Gray
        
        try {
            $body = @{ video_url = $videoUrl } | ConvertTo-Json
            $result = Invoke-RestMethod `
                -Uri "$baseUrl/api/analyze_video" `
                -Method Post `
                -ContentType "application/json" `
                -Body $body `
                -ErrorAction Stop
            
            Write-Host "`n" + "="*50
            Write-Host "ANALYSIS RESULTS" -ForegroundColor Green
            Write-Host "="*50
            
            Write-Host "`nTranscript Preview:" -ForegroundColor Cyan
            $preview = if ($result.transcript.Length -gt 200) { 
                $result.transcript.Substring(0, 200) + "..." 
            } else { 
                $result.transcript 
            }
            Write-Host "  $preview" -ForegroundColor White
            
            Write-Host "`nMetadata:" -ForegroundColor Cyan
            Write-Host "  Duration: $($result.metadata.duration_seconds) seconds"
            Write-Host "  Language: $($result.metadata.language_code)"
            Write-Host "  Confidence: $([math]::Round($result.metadata.confidence * 100, 1))%"
            Write-Host "  Word Count: $($result.metadata.word_count)"
            
            Write-Host "`nSafety Assessment:" -ForegroundColor Cyan
            if ($result.is_safe) {
                Write-Host "  ✅ SAFE for children under 6" -ForegroundColor Green
            } else {
                Write-Host "  ❌ NOT SAFE for children under 6" -ForegroundColor Red
            }
            Write-Host "  Verdict: $($result.gemini_verdict)"
            Write-Host "  Reason: $($result.reason)" -ForegroundColor Gray
            
            Write-Host "`n" + "="*50
            
        } catch {
            Write-Host "`n❌ Analysis failed:" -ForegroundColor Red
            $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
            Write-Host "  $($errorDetail.detail)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n⚠️ Invalid URL. Must start with 'gs://'" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nNo problem! Upload a video to GCS first:" -ForegroundColor Cyan
    Write-Host "  gsutil cp your-video.mp4 gs://your-bucket/your-video.mp4"
    Write-Host ""
}

Write-Host "`n✅ Test complete!" -ForegroundColor Green
