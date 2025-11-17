# Video Analysis API - Complete Guide

## 🎥 Overview

The Video Analysis API transcribes videos from Google Cloud Storage and uses Gemini AI to determine if the content is safe for children under 6 years old.

---

## 🚀 Quick Start

### 1. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key or use existing one
4. Copy the API key

### 2. Configure Environment

Add to your `.env` file:

```env
# Gemini AI Configuration
GEMINI_API_KEY=your-actual-gemini-api-key-here
```

### 3. Install Dependencies

```powershell
python -m pip install google-cloud-speech google-generativeai
```

Or install all requirements:

```powershell
python -m pip install -r requirements.txt
```

### 4. Restart Server

```powershell
# Stop the server (Ctrl+C) and restart
python -m uvicorn app.main:app --reload
```

---

## 📡 API Endpoint

### `POST /api/analyze_video`

Transcribe and analyze video content for child safety.

**Request Body:**
```json
{
  "video_url": "gs://bucket-name/video.mp4"
}
```

**Response (Safe Content):**
```json
{
  "transcript": "Hello kids! Today we're going to learn about animals. Let's start with elephants...",
  "metadata": {
    "duration_seconds": 125.5,
    "language_code": "en-US",
    "confidence": 0.95,
    "word_count": 250,
    "character_count": 1200,
    "model": "video",
    "enhanced": true
  },
  "is_safe": true,
  "reason": "The content is educational, age-appropriate, and contains no inappropriate language, violence, or adult themes. Perfect for children under 6.",
  "gemini_verdict": "YES"
}
```

**Response (Unsafe Content):**
```json
{
  "transcript": "This video contains explicit language and violent references...",
  "metadata": {
    "duration_seconds": 90.0,
    "language_code": "en-US",
    "confidence": 0.92
  },
  "is_safe": false,
  "reason": "The video contains profanity and references to violence which are not appropriate for children under 6.",
  "gemini_verdict": "NO"
}
```

---

## 🔧 How It Works

### Step 1: Video Transcription

The API uses **Google Cloud Speech-to-Text** with:

- **Model**: `video` (optimized for video content)
- **Enhanced**: Yes (higher accuracy)
- **Method**: `long_running_recognize` (async, handles long videos)
- **Features**:
  - Automatic punctuation
  - Word-level timestamps
  - Confidence scores
  - Multi-language support

### Step 2: Gemini AI Analysis

The transcript and metadata are sent to **Gemini Pro** with this prompt:

```
Analyze the following transcript and metadata from a video:

Transcript: [full transcript]
Metadata: [duration, language, confidence]

Is this video safe for children under age 6? Are there any abusive words, 
violence, sexual content, or inappropriate references?

Respond with YES or NO and include a brief explanation.

Format your response as:
VERDICT: [YES or NO]
EXPLANATION: [Your explanation here]
```

### Step 3: Safety Decision

- **YES** → `is_safe: true` → Content is appropriate
- **NO** → `is_safe: false` → Content should be filtered

---

## 💻 Usage Examples

### PowerShell

```powershell
# Analyze a video
$body = @{
    video_url = "gs://happyscroll-videos/kids-cartoon.mp4"
} | ConvertTo-Json

$result = Invoke-RestMethod `
    -Uri "http://localhost:8000/api/analyze_video" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

# Check if safe
if ($result.is_safe) {
    Write-Host "✅ Video is safe for kids" -ForegroundColor Green
    Write-Host "Reason: $($result.reason)"
} else {
    Write-Host "❌ Video is NOT safe for kids" -ForegroundColor Red
    Write-Host "Reason: $($result.reason)"
}
```

### Python

```python
import requests

# Analyze video
response = requests.post(
    "http://localhost:8000/api/analyze_video",
    json={"video_url": "gs://my-bucket/video.mp4"}
)

result = response.json()

print(f"Transcript: {result['transcript'][:100]}...")
print(f"Safe: {result['is_safe']}")
print(f"Reason: {result['reason']}")
```

### JavaScript

```javascript
async function analyzeVideo(videoUrl) {
  const response = await fetch('http://localhost:8000/api/analyze_video', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ video_url: videoUrl })
  });
  
  const result = await response.json();
  
  if (result.is_safe) {
    console.log('✅ Safe for kids:', result.reason);
  } else {
    console.log('❌ Not safe:', result.reason);
  }
  
  return result;
}

// Usage
analyzeVideo('gs://my-bucket/kids-video.mp4');
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/analyze_video" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "gs://my-bucket/video.mp4"}'
```

---

## 🎯 Testing

### Check Service Status

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video/status"
```

**Expected Response:**
```json
{
  "status": "ready",
  "service": "video_analysis",
  "components": {
    "speech_to_text": "configured",
    "gemini_ai": "configured"
  },
  "project_id": "your-project-id"
}
```

### Test with Sample Video

You'll need to:

1. Upload a test video to Google Cloud Storage
2. Get the `gs://` URL
3. Call the API with that URL

**Upload video to GCS:**
```powershell
# Using gsutil (if installed)
gsutil cp test-video.mp4 gs://your-bucket/test-video.mp4
```

---

## 📊 Response Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `transcript` | string | Full text transcription of the video audio |
| `metadata.duration_seconds` | number | Video duration in seconds |
| `metadata.language_code` | string | Detected language (e.g., "en-US") |
| `metadata.confidence` | number | Average transcription confidence (0-1) |
| `metadata.word_count` | number | Total words in transcript |
| `is_safe` | boolean | `true` if safe for kids, `false` otherwise |
| `reason` | string | Gemini's explanation for the verdict |
| `gemini_verdict` | string | Raw verdict: "YES" or "NO" |

---

## ⚠️ Error Handling

### Error: Missing video_url
```json
{
  "detail": "video_url cannot be empty"
}
```

### Error: Invalid URL format
```json
{
  "detail": "video_url must be a Google Cloud Storage URL starting with 'gs://'"
}
```

### Error: Transcription failed
```json
{
  "detail": "Transcription failed: Could not access video at gs://bucket/video.mp4"
}
```

### Error: Empty transcript
```json
{
  "detail": "Transcription returned empty result. The video may not contain any speech."
}
```

### Error: Gemini not configured
```json
{
  "detail": "GEMINI_API_KEY not set in environment"
}
```

---

## 🔒 Security & Best Practices

### 1. Secure API Keys

```env
# ❌ BAD: Hardcoded in code
gemini_api_key = "AIzaSyD..."

# ✅ GOOD: Environment variable
GEMINI_API_KEY=AIzaSyD...
```

### 2. Validate Video URLs

Only accept `gs://` URLs from trusted buckets:

```python
ALLOWED_BUCKETS = ["my-videos-bucket", "kids-content-bucket"]

def is_valid_url(video_url: str) -> bool:
    if not video_url.startswith("gs://"):
        return False
    
    bucket = video_url.split("/")[2]
    return bucket in ALLOWED_BUCKETS
```

### 3. Rate Limiting

Consider adding rate limits to prevent abuse:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/analyze_video")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def analyze_video(request: VideoAnalysisRequest):
    ...
```

### 4. Timeout Handling

Long videos can take several minutes:

```python
# Service already has 10-minute timeout
operation.result(timeout=600)  # 10 minutes
```

---

## 💰 Pricing

### Google Cloud Speech-to-Text

**Standard Model:**
- First 60 minutes/month: **FREE**
- After: **$0.006/15 seconds** ($1.44/hour)

**Enhanced Video Model (used by default):**
- First 60 minutes/month: **FREE**
- After: **$0.009/15 seconds** ($2.16/hour)

### Gemini AI

**Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- **FREE** for reasonable usage

**Paid Tier (if needed):**
- $0.00025 per 1K characters (input)
- $0.0005 per 1K characters (output)

### Example Costs

**10 videos, 2 minutes each:**
- Speech-to-Text: FREE (within 60 min/month)
- Gemini: FREE (within daily limits)
- **Total: $0.00**

**100 videos, 5 minutes each (500 min total):**
- Speech-to-Text: 60 min free + 440 min × $2.16/60 = **$15.84**
- Gemini: FREE (within limits)
- **Total: ~$16/month**

---

## 🚀 Advanced Configuration

### Custom Language Detection

```python
config = speech.RecognitionConfig(
    language_code="es-ES",  # Spanish
    alternative_language_codes=["en-US", "fr-FR"]
)
```

### Higher Accuracy

```python
config = speech.RecognitionConfig(
    use_enhanced=True,  # Use enhanced model
    model="video",      # Optimized for video
    enable_automatic_punctuation=True,
    enable_word_confidence=True
)
```

### Custom Gemini Prompt

Edit `video_analysis_service.py`:

```python
prompt = f"""Analyze this content for a {target_age_group} audience:

Transcript: {transcript}

Check for: violence, profanity, sexual content, scary themes

Respond: SAFE or UNSAFE with explanation.
"""
```

---

## 📚 API Documentation

Full interactive documentation available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try the `/api/analyze_video` endpoint directly in the browser!

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not set"

**Solution:**
1. Get API key from https://makersuite.google.com/app/apikey
2. Add to `.env`: `GEMINI_API_KEY=your-key-here`
3. Restart server

### Issue: "Could not access video"

**Solution:**
1. Verify video exists: `gsutil ls gs://bucket/video.mp4`
2. Check service account has Storage Object Viewer role
3. Ensure video is in correct format (MP4, MOV, etc.)

### Issue: "Empty transcript"

**Solution:**
- Video must contain audible speech
- Check audio quality and volume
- Try with a different video that has clear speech

### Issue: "Timeout waiting for operation"

**Solution:**
- Video is too long (>10 minutes)
- Increase timeout in `video_analysis_service.py`
- Consider splitting long videos

---

## ✅ Complete Example Workflow

```powershell
# 1. Check service status
Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video/status"

# 2. Upload video to GCS (if needed)
gsutil cp my-video.mp4 gs://my-bucket/my-video.mp4

# 3. Analyze video
$body = @{ video_url = "gs://my-bucket/my-video.mp4" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:8000/api/analyze_video" -Method Post -ContentType "application/json" -Body $body

# 4. Check results
Write-Host "Transcript: $($result.transcript.Substring(0, 100))..."
Write-Host "Duration: $($result.metadata.duration_seconds)s"
Write-Host "Safe: $($result.is_safe)"
Write-Host "Reason: $($result.reason)"
```

---

## 🎉 Success!

Your video analysis API is now ready to:

✅ Transcribe videos from Google Cloud Storage  
✅ Analyze content with Gemini AI  
✅ Determine child safety automatically  
✅ Provide detailed explanations  

Perfect for the HappyScroll Chrome extension! 🚀
