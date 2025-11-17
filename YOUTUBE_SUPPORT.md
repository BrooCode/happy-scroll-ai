# 🎬 YouTube Video Analysis - Quick Start Guide

## ✅ YES! You Can Use YouTube URLs!

The API now supports **both** Google Cloud Storage and YouTube URLs!

---

## 🚀 Quick Test

### 1. Ensure yt-dlp is installed:

```powershell
python -m pip install yt-dlp
```

### 2. Run the test script:

```powershell
.\test_youtube_analysis.ps1
```

---

## 📡 API Usage

### Analyze YouTube Video

**Request:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**PowerShell Example:**
```powershell
$body = @{
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
} | ConvertTo-Json

$result = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/analyze_video" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Write-Host "Safe: $($result.is_safe)"
Write-Host "Reason: $($result.reason)"
```

---

## 🎥 Supported URL Formats

### YouTube URLs ✅

```
✅ https://www.youtube.com/watch?v=VIDEO_ID
✅ https://youtu.be/VIDEO_ID
✅ https://www.youtube.com/shorts/SHORT_ID
✅ https://www.youtube.com/embed/VIDEO_ID
✅ https://m.youtube.com/watch?v=VIDEO_ID
```

### Google Cloud Storage URLs ✅

```
✅ gs://bucket-name/video.mp4
✅ gs://my-videos/kids/cartoon.mp4
```

---

## 🔧 How It Works

### For YouTube URLs:

1. **Download Audio** - Uses `yt-dlp` to extract audio as WAV format
2. **Upload to GCS** - Temporarily stores in `{project-id}-temp-audio` bucket
3. **Transcribe** - Google Cloud Speech-to-Text processes the audio
4. **Analyze** - Gemini AI evaluates content safety
5. **Cleanup** - Temporary files are automatically cleaned up

### For GCS URLs:

1. **Transcribe** - Directly processes video from GCS
2. **Analyze** - Gemini AI evaluates content safety

---

## ⚡ Performance

| Video Length | Download Time | Transcription Time | Total Time |
|--------------|---------------|-------------------|------------|
| 1 minute | ~10s | ~30s | ~40s |
| 3 minutes | ~20s | ~60s | ~80s |
| 5 minutes | ~30s | ~90s | ~120s |

**Note**: First-time downloads may be slower due to YouTube throttling.

---

## 💡 Real-World Examples

### Example 1: Music Video

```powershell
POST /api/analyze_video
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}

Response:
{
  "is_safe": true,
  "reason": "Music video with appropriate lyrics, no violence or inappropriate content",
  "gemini_verdict": "YES"
}
```

### Example 2: Kids Cartoon

```powershell
POST /api/analyze_video
{
  "video_url": "https://www.youtube.com/watch?v=KIDS_VIDEO_ID"
}

Response:
{
  "is_safe": true,
  "reason": "Educational cartoon with child-friendly content and language",
  "gemini_verdict": "YES"
}
```

### Example 3: Inappropriate Content

```powershell
POST /api/analyze_video
{
  "video_url": "https://www.youtube.com/watch?v=ADULT_VIDEO_ID"
}

Response:
{
  "is_safe": false,
  "reason": "Contains profanity and adult themes not suitable for children under 6",
  "gemini_verdict": "NO"
}
```

---

## 🚨 Troubleshooting

### Error: "yt-dlp not found"

**Solution:**
```powershell
# Install yt-dlp
python -m pip install yt-dlp

# Verify installation
yt-dlp --version
```

### Error: "Failed to download YouTube audio"

**Possible causes:**
1. Video is private/restricted
2. Video has age restrictions
3. Network issues
4. yt-dlp needs updating

**Solution:**
```powershell
# Update yt-dlp
python -m pip install --upgrade yt-dlp

# Test yt-dlp directly
yt-dlp -f bestaudio "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Error: "Transcription returned empty result"

**Cause**: Video has no speech/audio

**Solution**: Choose a video with clear speech audio

---

## 🎯 Use Cases

### HappyScroll Chrome Extension

```javascript
// In your extension
async function analyzeYouTubeVideo(videoId) {
  const youtubeUrl = `https://www.youtube.com/watch?v=${videoId}`;
  
  const response = await fetch('http://localhost:8000/api/analyze_video', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ video_url: youtubeUrl })
  });
  
  const result = await response.json();
  
  if (!result.is_safe) {
    // Skip this video
    console.log('⚠️ Unsafe content detected:', result.reason);
    skipToNextVideo();
  }
  
  return result;
}

// Usage
const videoId = new URL(window.location.href).searchParams.get('v');
await analyzeYouTubeVideo(videoId);
```

### Bulk Analysis Script

```powershell
# Analyze multiple videos
$videos = @(
    "https://www.youtube.com/watch?v=VIDEO_1",
    "https://www.youtube.com/watch?v=VIDEO_2",
    "https://www.youtube.com/watch?v=VIDEO_3"
)

$results = @()
foreach ($video in $videos) {
    Write-Host "Analyzing: $video"
    $body = @{ video_url = $video } | ConvertTo-Json
    $result = Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" -Method Post -ContentType "application/json" -Body $body
    $results += $result
}

# Show summary
$safe = ($results | Where-Object { $_.is_safe }).Count
$unsafe = ($results | Where-Object { -not $_.is_safe }).Count
Write-Host "`nSummary: $safe safe, $unsafe unsafe out of $($videos.Count) videos"
```

---

## 💰 Cost Considerations

### YouTube Downloads
- **Free** - yt-dlp is open source

### Google Cloud Storage (temporary)
- **~$0.02/GB/month** - Storage cost (auto-cleanup recommended)
- **~$0.12/GB** - Network egress (minimal for audio files)

### Speech-to-Text
- First 60 min/month: **FREE**
- After: **~$2.16/hour**

### Gemini AI
- 60 requests/min: **FREE**
- 1,500 requests/day: **FREE**

**Example**: Analyzing 100 YouTube videos (3 min each):
- Download: $0 (yt-dlp is free)
- Storage: $0.01 (temporary, cleaned up)
- Transcription: ~$11 (300 minutes)
- Gemini: $0 (within free tier)
**Total: ~$11**

---

## 🔐 Security Notes

1. **Temporary Storage**: Audio files are stored temporarily in GCS and should be cleaned up
2. **Rate Limiting**: Consider adding rate limits to prevent abuse
3. **URL Validation**: The API validates YouTube and GCS URLs
4. **Timeout Protection**: 5-minute timeout for downloads

---

## ✅ Summary

**Before**: Only supported `gs://bucket/video.mp4`

**Now**: Supports:
- ✅ YouTube URLs (any format)
- ✅ Google Cloud Storage URLs
- ✅ Automatic audio extraction
- ✅ Temporary storage management

**Perfect for HappyScroll!** Now you can analyze YouTube Shorts directly! 🎉

---

## 📚 Additional Resources

- **yt-dlp docs**: https://github.com/yt-dlp/yt-dlp
- **Speech-to-Text**: https://cloud.google.com/speech-to-text/docs
- **Gemini AI**: https://ai.google.dev/docs

---

**Ready to test?** Run: `.\test_youtube_analysis.ps1` 🚀
