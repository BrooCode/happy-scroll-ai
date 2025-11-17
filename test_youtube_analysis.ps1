# YouTube Video Analysis Test
# Test the video analysis endpoint with YouTube URLs

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "YouTube Video Analysis - Quick Test" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000"

# Check if server is running
Write-Host "`nChecking server status..." -NoNewline
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/api/health" -ErrorAction Stop
    Write-Host " ✅" -ForegroundColor Green
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "Server not running. Start with: python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
    exit 1
}

# Check video analysis service
Write-Host "Checking video analysis service..." -NoNewline
try {
    $status = Invoke-RestMethod -Uri "$baseUrl/api/analyze_video/status" -ErrorAction Stop
    if ($status.status -eq "ready") {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ⚠️ $($status.status)" -ForegroundColor Yellow
        if ($status.message) {
            Write-Host "  $($status.message)" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + "="*50
Write-Host "YOUTUBE VIDEO ANALYSIS" -ForegroundColor Cyan
Write-Host "="*50

# Sample YouTube URLs for testing
$testVideos = @(
    @{
        name = "Rick Astley - Never Gonna Give You Up"
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        expected = "Safe (music video)"
    },
    @{
        name = "Short URL format"
        url = "https://youtu.be/dQw4w9WgXcQ"
        expected = "Safe (music video)"
    }
)

Write-Host "`nAvailable test videos:" -ForegroundColor Yellow
for ($i = 0; $i -lt $testVideos.Count; $i++) {
    Write-Host "  $($i + 1). $($testVideos[$i].name)"
    Write-Host "     URL: $($testVideos[$i].url)" -ForegroundColor Gray
}

Write-Host "`nEnter video number to test (1-$($testVideos.Count)), or paste your own YouTube URL: " -NoNewline -ForegroundColor Yellow
$input = Read-Host

$videoUrl = ""
if ($input -match '^\d+$') {
    $index = [int]$input - 1
    if ($index -ge 0 -and $index -lt $testVideos.Count) {
        $videoUrl = $testVideos[$index].url
        Write-Host "`nTesting: $($testVideos[$index].name)" -ForegroundColor Cyan
    } else {
        Write-Host "Invalid selection" -ForegroundColor Red
        exit 1
    }
} elseif ($input -match 'youtube\.com|youtu\.be') {
    $videoUrl = $input
    Write-Host "`nTesting custom URL: $videoUrl" -ForegroundColor Cyan
} else {
    Write-Host "Invalid input" -ForegroundColor Red
    exit 1
}

Write-Host "`n⏳ Analyzing video (this may take several minutes)..." -ForegroundColor Yellow
Write-Host "   - Downloading audio from YouTube"
Write-Host "   - Uploading to Google Cloud Storage"
Write-Host "   - Transcribing with Speech-to-Text"
Write-Host "   - Analyzing with Gemini AI"
Write-Host ""

try {
    $body = @{ video_url = $videoUrl } | ConvertTo-Json
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    $result = Invoke-RestMethod `
        -Uri "$baseUrl/api/analyze_video" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop
    
    $stopwatch.Stop()
    $elapsed = $stopwatch.Elapsed.TotalSeconds
    
    Write-Host "="*50
    Write-Host "✅ ANALYSIS COMPLETE ($([math]::Round($elapsed, 1))s)" -ForegroundColor Green
    Write-Host "="*50
    
    Write-Host "`nTranscript Preview:" -ForegroundColor Cyan
    $preview = if ($result.transcript.Length -gt 300) {
        $result.transcript.Substring(0, 300) + "..."
    } else {
        $result.transcript
    }
    Write-Host "  `"$preview`"" -ForegroundColor White
    
    Write-Host "`nMetadata:" -ForegroundColor Cyan
    Write-Host "  Duration: $($result.metadata.duration_seconds) seconds"
    Write-Host "  Language: $($result.metadata.language_code)"
    Write-Host "  Confidence: $([math]::Round($result.metadata.confidence * 100, 1))%"
    Write-Host "  Word Count: $($result.metadata.word_count)"
    
    Write-Host "`nSafety Assessment:" -ForegroundColor Cyan
    if ($result.is_safe) {
        Write-Host "  ✅ SAFE for children under 6" -ForegroundColor Green -BackgroundColor DarkGreen
    } else {
        Write-Host "  ❌ NOT SAFE for children under 6" -ForegroundColor White -BackgroundColor Red
    }
    Write-Host ""
    Write-Host "  Gemini Verdict: $($result.gemini_verdict)" -ForegroundColor Yellow
    Write-Host "  Reason:" -ForegroundColor Gray
    Write-Host "    $($result.reason)" -ForegroundColor White
    
    Write-Host "`n" + "="*50
    
} catch {
    Write-Host "`n❌ ANALYSIS FAILED" -ForegroundColor Red
    Write-Host "="*50
    
    try {
        $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "Error: $($errorDetail.detail)" -ForegroundColor Yellow
    } catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host "`n💡 Tip: You can analyze any YouTube video by pasting its URL!" -ForegroundColor Cyan
Write-Host "Examples:" -ForegroundColor Gray
Write-Host "  - https://www.youtube.com/watch?v=VIDEO_ID"
Write-Host "  - https://youtu.be/VIDEO_ID"
Write-Host "  - https://www.youtube.com/shorts/SHORT_ID"
Write-Host ""
