# YouTube Video Analysis - Quick Start Guide

## 🎯 What This Does

Analyze YouTube videos for content safety by:
1. Downloading audio from YouTube
2. Transcribing speech to text
3. Analyzing content with Google Gemini AI

## ⚡ Quick Start

### 1. Install FFmpeg (One-Time Setup)

FFmpeg is required to extract audio from YouTube videos.

**Automated Setup (Recommended):**
```powershell
.\setup_ffmpeg.ps1
```

This will:
- Download FFmpeg (~80 MB)
- Extract to `.\ffmpeg\bin\`
- Verify installation
- No system PATH changes needed!

**Manual Setup:**
If the script doesn't work, download manually:
1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extract the zip file
3. Rename the extracted folder to `ffmpeg` 
4. Move to project root: `D:\happy-scroll-ai\ffmpeg\`

Verify: `.\ffmpeg\bin\ffmpeg.exe -version`

### 2. Configure API Keys

Make sure your `.env` file has:
```env
GEMINI_API_KEY=your-actual-gemini-key
GOOGLE_APPLICATION_CREDENTIALS=./credentials/your-service-account.json
```

### 3. Start the Server

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test with YouTube URL

**Option A: Interactive Test Script**
```powershell
.\test_youtube_analysis.ps1
```

**Option B: Direct API Call**
```powershell
$body = @{
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Option C: Browser**
1. Open: http://localhost:8000/docs
2. Try the `/api/analyze_video` endpoint
3. Paste a YouTube URL

## 📝 Supported URL Formats

All these work:
```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
https://m.youtube.com/watch?v=VIDEO_ID
```

## ⏱️ Processing Time

| Video Length | Approximate Time |
|--------------|------------------|
| 1-3 minutes  | 1-2 minutes      |
| 5-10 minutes | 3-7 minutes      |
| 15-30 minutes| 10-20 minutes    |

**Note:** The API waits for complete processing before responding.

## 🔍 What You Get

```json
{
  "video_url": "https://youtube.com/...",
  "transcript": {
    "text": "Full transcription...",
    "language": "en-US",
    "confidence": 0.95,
    "duration_seconds": 180.5,
    "word_count": 450
  },
  "safety_analysis": {
    "is_safe": true,
    "safety_categories": {
      "hate_speech": {"detected": false, "confidence": "high"},
      "violence": {"detected": false, "confidence": "high"},
      "sexual_content": {"detected": false, "confidence": "high"},
      "dangerous_content": {"detected": false, "confidence": "high"}
    },
    "overall_score": 0.95,
    "summary": "Content analysis summary..."
  },
  "processing_time_seconds": 45.2
}
```

## 🛠️ Troubleshooting

### Error: "ffmpeg not found"
- Run `.\setup_ffmpeg.ps1` again
- Verify: `.\ffmpeg\bin\ffmpeg.exe -version`
- Make sure `ffmpeg` folder is in project root

### Error: "Failed to download YouTube audio"
- Check internet connection
- Verify YouTube URL is valid
- Some videos may be geo-restricted or age-restricted

### Error: "Google Cloud credentials not found"
- Check `.env` file has correct path
- Verify service account JSON exists
- Ensure proper permissions (Speech-to-Text, Storage)

### Error: "Gemini API key invalid"
- Get key from: https://makersuite.google.com/app/apikey
- Update `.env` file with real key
- Restart the server

### Slow Processing
- Normal for longer videos (see processing time table above)
- Speech-to-Text processes at ~1x video speed
- Consider implementing async processing for videos >5 minutes

## 📊 Cost Estimation

**Per 10-minute video:**
- YouTube download: Free
- Google Cloud Storage: ~$0.001 (temporary storage)
- Speech-to-Text: ~$0.024 (standard model)
- Gemini API: ~$0.001 (per 1000 tokens)

**Total: ~$0.026 per 10-minute video**

## 🚀 Next Steps

1. **Implement async processing** for longer videos
2. **Add webhook callbacks** for completion notifications
3. **Cache transcripts** to avoid re-processing
4. **Add cleanup jobs** for temporary GCS files
5. **Batch processing** for multiple videos

## 📚 Related Documentation

- [YOUTUBE_SUPPORT.md](./YOUTUBE_SUPPORT.md) - Detailed technical docs
- [VIDEO_ANALYSIS_API.md](./VIDEO_ANALYSIS_API.md) - API specification
- [INSTALL_FFMPEG.md](./INSTALL_FFMPEG.md) - FFmpeg installation guide
- [GOOGLE_CLOUD_SETUP.md](./GOOGLE_CLOUD_SETUP.md) - GCP setup

## 🆘 Need Help?

Check the server logs for detailed error messages:
- The terminal running uvicorn shows real-time logs
- Look for ERROR or WARNING messages
- Full stack traces are included

Server running at: http://localhost:8000
API docs at: http://localhost:8000/docs
