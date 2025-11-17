# FFmpeg Manual Installation Guide

The automated download is experiencing issues. Please follow these simple manual steps:

## Option 1: Direct Download & Extract (5 minutes)

### Step 1: Download FFmpeg

Click this link to download:
**https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip**

Or use this alternative:
**https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip**

### Step 2: Extract the ZIP file

1. Right-click the downloaded `ffmpeg-....zip` file
2. Select "Extract All..."
3. Extract to your Downloads folder

### Step 3: Move to Project

1. Open the extracted folder
2. Find the folder that contains a `bin` subfolder with `ffmpeg.exe` and `ffprobe.exe`
3. Rename this folder to just `ffmpeg`
4. Move/Copy the `ffmpeg` folder to: `D:\happy-scroll-ai\`

Final structure should be:
```
D:\happy-scroll-ai\
  ├── ffmpeg\
  │   ├── bin\
  │   │   ├── ffmpeg.exe
  │   │   └── ffprobe.exe
  │   └── ... (other files)
  ├── app\
  ├── ... (other project files)
```

### Step 4: Verify Installation

Open PowerShell in the project directory and run:
```powershell
.\ffmpeg\bin\ffmpeg.exe -version
```

You should see FFmpeg version information.

## Option 2: Use Chocolatey (If Installed)

If you have Chocolatey package manager:
```powershell
choco install ffmpeg
```

Then the system FFmpeg will be used automatically.

## Option 3: Use Winget (Windows 10/11)

If you have Winget:
```powershell
winget install Gyan.FFmpeg
```

This installs FFmpeg system-wide.

## After Installation

### Test the YouTube Analysis

The server is already running and will automatically detect FFmpeg in the `ffmpeg/bin/` folder.

Just run:
```powershell
.\test_youtube_analysis.ps1
```

Or test directly:
```powershell
$body = @{
    video_url = "https://www.youtube.com/shorts/JkV-BbqA6L0"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

## Verification Steps

1. ✅ FFmpeg folder exists: `Test-Path ".\ffmpeg\bin\ffmpeg.exe"`
2. ✅ FFmpeg works: `.\ffmpeg\bin\ffmpeg.exe -version`
3. ✅ Server is running: Check http://localhost:8000/docs
4. ✅ Try YouTube URL in the API

## Troubleshooting

**"Cannot find ffmpeg.exe"**
- Make sure the path is exactly: `D:\happy-scroll-ai\ffmpeg\bin\ffmpeg.exe`
- Check folder names (should be lowercase 'ffmpeg', not 'FFmpeg')

**"Access is denied"**
- Extract as Administrator
- Or extract to Downloads first, then move

**Still not working?**
The code is already updated to automatically find FFmpeg in the project directory.
If FFmpeg is in `D:\happy-scroll-ai\ffmpeg\bin\`, it will be detected automatically.

No need to restart the server - it auto-reloads!

## Quick Test Command

Once FFmpeg is in place, run this to test everything:
```powershell
# Test 1: Check FFmpeg
.\ffmpeg\bin\ffmpeg.exe -version

# Test 2: Check server
curl http://localhost:8000/docs

# Test 3: Try YouTube analysis
.\test_youtube_analysis.ps1
```

## Need Help?

If you're still stuck, just let me know:
1. Where did you extract FFmpeg?
2. What error are you seeing?
3. Run: `Get-ChildItem -Recurse -Filter "ffmpeg.exe" | Select-Object FullName`

This will help me locate the file and guide you further!
