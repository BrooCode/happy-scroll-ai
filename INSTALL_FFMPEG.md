# Installing FFmpeg for YouTube Audio Processing

FFmpeg is required for yt-dlp to convert YouTube audio to WAV format.

## Quick Installation Options

### Option 1: Using Winget (Recommended - Windows 10/11)
```powershell
winget install Gyan.FFmpeg
```

### Option 2: Using Chocolatey
```powershell
choco install ffmpeg
```

### Option 3: Manual Installation

1. **Download FFmpeg:**
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`
   - Or direct link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z

2. **Extract the archive:**
   - Extract to: `C:\ffmpeg`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH:**
   ```powershell
   # Run PowerShell as Administrator
   $env:Path += ";C:\ffmpeg\bin"
   [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)
   ```

4. **Verify installation:**
   ```powershell
   ffmpeg -version
   ```

## Alternative: Use FFmpeg Portable (No Installation)

If you can't modify PATH, you can tell yt-dlp where FFmpeg is located:

1. Download FFmpeg portable
2. Extract to `D:\happy-scroll-ai\ffmpeg\`
3. Update the code to specify FFmpeg location

## After Installation

1. **Close and reopen** your terminal/PowerShell
2. **Verify FFmpeg is working:**
   ```powershell
   ffmpeg -version
   python -m yt_dlp --version
   ```

3. **Restart the FastAPI server:**
   ```powershell
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Test YouTube Analysis

Once FFmpeg is installed, test with:
```powershell
.\test_youtube_analysis.ps1
```

Or manually:
```powershell
$body = @{
    video_url = "https://www.youtube.com/shorts/JkV-BbqA6L0"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" -Method POST -Body $body -ContentType "application/json"
```

## Troubleshooting

**Error: "ffmpeg not found"**
- Make sure ffmpeg.exe is in your PATH
- Restart your terminal/PowerShell after installation
- Try running: `where.exe ffmpeg` to check if it's found

**Error: "ffprobe and ffmpeg not found"**
- Both ffmpeg.exe and ffprobe.exe need to be in PATH
- They're both included in the FFmpeg download

**Still not working?**
- Download the portable version
- Place in project directory: `D:\happy-scroll-ai\ffmpeg\bin\`
- We can modify the code to use this specific location
