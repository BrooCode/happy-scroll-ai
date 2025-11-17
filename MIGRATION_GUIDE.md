# Migration Guide: OpenAI → Google Cloud Vision

## 🔄 Overview

This document outlines the changes when migrating from OpenAI moderation to Google Cloud Vision API.

---

## 📊 Key Differences

| Feature | OpenAI (Old) | Google Cloud Vision (New) |
|---------|--------------|---------------------------|
| **Input Type** | Text content | Image URLs |
| **Pricing** | $0.20 per 1K tokens | $1.50 per 1K images (after free tier) |
| **Free Tier** | None | 1,000 images/month |
| **Rate Limits** | 3-5 req/min (free) | 1,800 req/min |
| **Response Time** | ~500ms | ~300-500ms |
| **Categories** | 11 categories | 5 SafeSearch categories |
| **Best For** | Text moderation | Image/thumbnail moderation |

---

## 🔧 Breaking Changes

### 1. API Request Format

**Old (OpenAI)**:
```json
{
  "content": "This is the text to moderate"
}
```

**New (Google Cloud Vision)**:
```json
{
  "image_url": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"
}
```

### 2. Response Format

**Old Response**:
```json
{
  "allowed": true,
  "safe": true,
  "categories": {
    "sexual": false,
    "hate": false,
    "violence": false,
    "self_harm": false
  }
}
```

**New Response**:
```json
{
  "allowed": true,
  "safe": true,
  "categories": {
    "adult": false,
    "violence": false,
    "racy": false,
    "medical": false,
    "spoof": false
  },
  "likelihood_scores": {
    "adult": "VERY_UNLIKELY",
    "violence": "UNLIKELY",
    "racy": "VERY_UNLIKELY",
    "medical": "UNLIKELY",
    "spoof": "VERY_UNLIKELY"
  },
  "threshold": "POSSIBLE",
  "service": "google_cloud_vision"
}
```

### 3. Environment Variables

**Old `.env`**:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**New `.env`**:
```env
GOOGLE_APPLICATION_CREDENTIALS=d:\happy-scroll-ai\credentials\service-account-key.json
GOOGLE_CLOUD_PROJECT=your-project-id
SAFETY_THRESHOLD=POSSIBLE
```

### 4. Dependencies

**Removed**:
```txt
openai==1.12.0
```

**Added**:
```txt
google-cloud-vision==3.7.0
google-cloud-videointelligence==2.13.0
pillow==10.2.0
aiohttp==3.9.3
```

---

## 📝 Code Changes Required

### Browser Extension (manifest.json)

No changes needed! The API endpoint remains the same.

### JavaScript Fetch Calls

**Change**:
```javascript
// OLD
const response = await fetch('http://localhost:8000/api/moderate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    content: videoTitle + " " + videoDescription // ❌ OLD
  })
});

// NEW
const response = await fetch('http://localhost:8000/api/moderate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    image_url: thumbnailUrl // ✅ NEW
  })
});
```

### Chrome Extension Content Script

**Old approach** (text-based):
```javascript
const title = document.querySelector('h1').textContent;
const description = document.querySelector('#description').textContent;
const content = title + " " + description;
```

**New approach** (image-based):
```javascript
// Get YouTube thumbnail URL
const videoId = new URL(window.location.href).searchParams.get('v');
const thumbnailUrl = `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg`;

// Or extract from page
const thumbnail = document.querySelector('meta[property="og:image"]')?.content;
```

---

## 🚀 Migration Steps

### Step 1: Update Your Extension

If your extension sends text content:

```javascript
// content.js - OLD
function getTitleAndDescription() {
  const title = document.querySelector('h1').textContent;
  return { content: title };
}

// content.js - NEW
function getThumbnailUrl() {
  // YouTube Shorts
  const videoId = window.location.pathname.split('/shorts/')[1];
  return { 
    image_url: `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg` 
  };
}
```

### Step 2: Update Backend

```powershell
# Stop running server
# Ctrl+C

# Pull latest changes (if using git)
git pull origin main

# Install new dependencies
python -m pip install -r requirements.txt

# Update .env file (see GOOGLE_CLOUD_SETUP.md)
# Add Google Cloud credentials

# Restart server
python -m uvicorn app.main:app --reload
```

### Step 3: Test New Integration

```powershell
# Test with a safe image
$body = @{
    image_url = "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" -Method Post -ContentType "application/json" -Body $body
```

---

## ⚠️ Compatibility Notes

### What Still Works

✅ **API Endpoint**: `/api/moderate` remains the same
✅ **Response Structure**: `allowed` and `safe` fields unchanged
✅ **HTTP Methods**: Still uses POST
✅ **CORS**: No changes needed

### What Changed

❌ **Request Body**: Must use `image_url` instead of `content`
❌ **Category Names**: Different categories (adult, racy, etc. vs sexual, hate, etc.)
⚠️ **Input Type**: Now requires image URLs, not text

---

## 💡 Why Migrate?

### Benefits

1. **Better Rate Limits**: 1,800 req/min vs 3-5 req/min
2. **Free Tier**: 1,000 images/month free
3. **Lower Cost**: ~$1.50/1K vs ~$10/1K for similar volume
4. **More Reliable**: No "429 Too Many Requests" errors
5. **Purpose-Built**: SafeSearch designed for visual content
6. **Faster**: Slightly better latency

### Trade-offs

1. **Image-Only**: Can't moderate text content directly
2. **New Setup**: Requires Google Cloud account
3. **Credentials**: More complex than API key

---

## 🎯 Use Case Recommendations

### ✅ Use Google Cloud Vision For:

- YouTube thumbnail moderation
- Image-heavy content filtering
- High-volume moderation (>100 req/hour)
- Cost-sensitive applications
- Real-time video thumbnail checks

### 🤔 Consider Alternatives For:

- **Text-only moderation**: Keep OpenAI or use Perspective API
- **Audio moderation**: Use specialized audio APIs
- **Complex context analysis**: GPT-4 Vision (more expensive but understands context)

---

## 📚 Additional Resources

- **Setup Guide**: `GOOGLE_CLOUD_SETUP.md`
- **Google Cloud Vision Docs**: https://cloud.google.com/vision/docs
- **SafeSearch API**: https://cloud.google.com/vision/docs/detecting-safe-search

---

## 🐛 Common Issues After Migration

### Issue 1: Extension Not Sending Images

**Problem**: Extension still sends text content

**Solution**:
```javascript
// Make sure you're extracting image URLs
const getThumbnail = () => {
  // YouTube
  const videoId = new URLSearchParams(window.location.search).get('v');
  if (videoId) {
    return `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg`;
  }
  
  // Or from meta tags
  return document.querySelector('meta[property="og:image"]')?.content;
};
```

### Issue 2: CORS Errors

**Problem**: Extension can't reach API

**Solution**: Check `app/main.py` has CORS enabled:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 3: "Invalid credentials"

**Problem**: Google Cloud credentials not loading

**Solution**:
1. Check `.env` file has correct path
2. Verify JSON key file exists
3. Restart the server

---

## ✅ Verification Checklist

- [ ] Google Cloud project created
- [ ] Vision API enabled
- [ ] Service account key downloaded
- [ ] `.env` file updated with credentials
- [ ] New dependencies installed
- [ ] Backend server restarts successfully
- [ ] Test API call returns expected response
- [ ] Extension updated to send `image_url`
- [ ] End-to-end test passes

---

**Migration complete! You're now using Google Cloud Vision for content moderation.** 🎉
