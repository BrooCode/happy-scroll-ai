# Quick Start Guide - YouTube Moderation

## ⚡ 60-Second Setup

### 1. Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test YouTube Moderation
```bash
curl -X POST "http://localhost:8000/api/moderate" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### 3. Expected Response
```json
{
  "allowed": true,
  "safe": true,
  "reason": "Content is safe. No inappropriate content detected.",
  "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "video_title": "Rick Astley - Never Gonna Give You Up",
  "channel_title": "Rick Astley"
}
```

---

## 🎯 Two Usage Modes

### Mode 1: YouTube URL
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### Mode 2: Direct Image URL
```json
{
  "image_url": "https://example.com/image.jpg"
}
```

---

## 🧪 Run Tests
```bash
python test_youtube_moderation.py
```

---

## 📖 Full Documentation
- **Complete Guide**: `YOUTUBE_MODERATION_FEATURE.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`
- **API Docs**: http://localhost:8000/docs

---

## ✅ Supported YouTube URLs
```
✅ youtube.com/watch?v=VIDEO_ID
✅ youtu.be/VIDEO_ID
✅ youtube.com/shorts/VIDEO_ID
✅ youtube.com/embed/VIDEO_ID
```

---

## 🔑 Environment Variables (Already Configured)
```properties
YOUTUBE_API_KEY=***YOUTUBE_KEY_REMOVED*** ✅
GOOGLE_APPLICATION_CREDENTIALS=D:\happy-scroll-ai\happyscroll-478318-6a860e981468.json ✅
GEMINI_API_KEY=***GEMINI_KEY_REMOVED*** ✅
```

---

## 🚀 That's It!
Your YouTube moderation endpoint is ready to use!
