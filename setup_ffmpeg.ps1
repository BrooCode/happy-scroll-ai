# FFmpeg Setup Script for HappyScroll AI
# This script downloads and sets up FFmpeg for YouTube audio processing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FFmpeg Setup for HappyScroll AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ffmpegDir = ".\ffmpeg"
$ffmpegBin = "$ffmpegDir\bin"
$downloadUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zipFile = "ffmpeg.zip"

# Check if already installed
if (Test-Path "$ffmpegBin\ffmpeg.exe") {
    Write-Host "✓ FFmpeg already installed at: $ffmpegBin" -ForegroundColor Green
    Write-Host ""
    & "$ffmpegBin\ffmpeg.exe" -version | Select-Object -First 1
    Write-Host ""
    Write-Host "✓ Setup complete! You can now use YouTube URLs." -ForegroundColor Green
    exit 0
}

Write-Host "Step 1: Downloading FFmpeg..." -ForegroundColor Yellow
Write-Host "URL: $downloadUrl" -ForegroundColor Gray
Write-Host "Size: ~80 MB (this may take 1-2 minutes)" -ForegroundColor Gray
Write-Host ""

try {
    # Download with progress
    $ProgressPreference = 'Continue'
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile -UseBasicParsing
    
    if (Test-Path $zipFile) {
        $fileSize = (Get-Item $zipFile).Length / 1MB
        Write-Host "✓ Downloaded successfully ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
    } else {
        throw "Download failed - file not found"
    }
} catch {
    Write-Host "✗ Download failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please download manually from:" -ForegroundColor Yellow
    Write-Host "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Then run:" -ForegroundColor Yellow
    Write-Host "  Expand-Archive -Path ffmpeg.zip -DestinationPath ." -ForegroundColor Cyan
    Write-Host "  Rename-Item ffmpeg-*-essentials_build ffmpeg" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "Step 2: Extracting FFmpeg..." -ForegroundColor Yellow

try {
    # Extract the zip file
    Expand-Archive -Path $zipFile -DestinationPath "." -Force
    
    # Find the extracted directory (it has a version number in the name)
    $extractedDir = Get-ChildItem -Directory -Filter "ffmpeg-*-essentials_build" | Select-Object -First 1
    
    if ($extractedDir) {
        # Rename to simple 'ffmpeg' directory
        if (Test-Path $ffmpegDir) {
            Remove-Item $ffmpegDir -Recurse -Force
        }
        Rename-Item $extractedDir.Name $ffmpegDir
        Write-Host "✓ Extracted successfully" -ForegroundColor Green
    } else {
        throw "Extraction failed - directory not found"
    }
} catch {
    Write-Host "✗ Extraction failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Cleaning up..." -ForegroundColor Yellow

try {
    # Remove the zip file
    Remove-Item $zipFile -Force
    Write-Host "✓ Cleaned up temporary files" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not remove temporary files" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 4: Verifying installation..." -ForegroundColor Yellow

if ((Test-Path "$ffmpegBin\ffmpeg.exe") -and (Test-Path "$ffmpegBin\ffprobe.exe")) {
    Write-Host "✓ FFmpeg installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Location: $ffmpegBin" -ForegroundColor Gray
    Write-Host ""
    
    # Show version
    & "$ffmpegBin\ffmpeg.exe" -version | Select-Object -First 1
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now analyze YouTube videos!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The server will automatically use this FFmpeg installation." -ForegroundColor Gray
    Write-Host "No need to restart - the changes are already active." -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "✗ Installation verification failed" -ForegroundColor Red
    Write-Host "Expected files not found in: $ffmpegBin" -ForegroundColor Red
    exit 1
}
