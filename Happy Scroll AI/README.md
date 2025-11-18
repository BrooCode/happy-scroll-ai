# Happy Scroll AI - Chrome Extension

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Manifest](https://img.shields.io/badge/manifest-v3-green.svg)

Automatically skips unsafe YouTube Shorts using AI-powered content moderation.

## 🎯 Features

- ✅ Automatic detection of YouTube Shorts
- ✅ Real-time safety checking via Happy Scroll AI API
- ✅ Auto-skip unsafe videos
- ✅ Detailed console logging for debugging
- ✅ 2-second delay before checking (ensures page is fully loaded)
- ✅ Single Page Application (SPA) navigation support

## 📋 Prerequisites

Before installing the extension, make sure:

1. **Happy Scroll AI API is running** on `http://localhost:8000`
   ```bash
   # Navigate to your API directory
   cd d:\happy-scroll-ai
   
   # Start the API server
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **CORS is enabled** in your FastAPI backend (see instructions below)

3. **Google Chrome** or **Microsoft Edge** browser (Chromium-based)

## 🚀 Installation Instructions

### Step 1: Prepare the Extension

1. The extension files are located in: `d:\happy-scroll-ai\Happy Scroll AI\`
2. You should see these files:
   - `manifest.json`
   - `content.js`
   - `background.js`
   - `icon.png`
   - `README.md`

### Step 2: Enable CORS in FastAPI Backend

Update your FastAPI `main.py` to allow Chrome extension requests:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",  # Allow Chrome extensions
        "http://localhost:*",     # Allow localhost
        "http://127.0.0.1:*"     # Allow 127.0.0.1
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of your API code
```

### Step 3: Load Extension in Chrome

1. Open Google Chrome
2. Navigate to: `chrome://extensions/`
3. Enable **Developer mode** (toggle in top-right corner)
4. Click **"Load unpacked"**
5. Select the folder: `d:\happy-scroll-ai\Happy Scroll AI`
6. The extension should now appear in your extensions list

### Step 4: Verify Installation

1. You should see "Happy Scroll AI" in your extensions
2. Click the puzzle icon (🧩) in Chrome toolbar
3. Pin "Happy Scroll AI" for easy access
4. The extension icon should be visible

## 🎮 How to Use

1. **Start your API server**:
   ```bash
   cd d:\happy-scroll-ai
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Navigate to YouTube Shorts**:
   - Go to: https://www.youtube.com/shorts
   - Or open any specific Short video

3. **Automatic Protection**:
   - The extension automatically checks each Short
   - If unsafe: automatically skips to next video
   - If safe: video plays normally

4. **Monitor Activity** (Optional):
   - Right-click on the page → Inspect (or press F12)
   - Go to the **Console** tab
   - Look for `[Happy Scroll AI]` messages

## 🔍 Debugging

### Check Console Logs

Open Chrome DevTools (F12) and look for these messages:

```
✅ Safe Video:
[Happy Scroll AI] ✅ Video is SAFE - Continuing playback

⚠️ Unsafe Video:
[Happy Scroll AI] ⚠️ UNSAFE VIDEO DETECTED - Skipping to next Short
[Happy Scroll AI] Reason: [reasons from API]

🔧 API Issues:
[Happy Scroll AI] API error: 404 Not Found
[Happy Scroll AI] Failed to check video safety: [error]
```

### Common Issues & Solutions

#### 1. Extension Not Working
- **Check**: Is the API running? Visit http://localhost:8000/docs
- **Check**: Are you on a YouTube Shorts page? (URL must contain `/shorts/`)
- **Check**: Open Console (F12) - any errors?

#### 2. CORS Errors
```
Access to fetch at 'http://localhost:8000/...' has been blocked by CORS policy
```
**Solution**: Add CORS middleware to your FastAPI app (see Step 2)

#### 3. API Not Responding
- **Check**: API server is running
- **Check**: Endpoint is correct: `http://localhost:8000/api/happyScroll/v1/verdict`
- **Test**: Try the API directly in browser

#### 4. Videos Not Skipping
- **Check**: The "Next" button exists on the page
- **Check**: Video was actually marked as unsafe by API
- **Check**: Console logs show the skip attempt

## 🛠️ Configuration

### Change API Endpoint

Edit `content.js` line 9:
```javascript
const API_ENDPOINT = 'http://localhost:8000/api/happyScroll/v1/verdict';
```

### Change Delay Time

Edit `content.js` line 10:
```javascript
const PAGE_LOAD_DELAY = 2000; // Change to desired milliseconds
```

### Important: API Uses POST Method

The extension sends POST requests with JSON body:
```javascript
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Do NOT use GET requests - they will return "Method Not Allowed" error.

## 📁 File Structure

```
Happy Scroll AI/
├── manifest.json      # Extension configuration (Manifest V3)
├── content.js         # Main logic - runs on YouTube pages
├── background.js      # Service worker - handles extension lifecycle
├── icon.png          # Extension icon (placeholder)
└── README.md         # This file
```

## 🔐 Permissions Explained

The extension requests these permissions:

- **activeTab**: Access to current YouTube tab
- **scripting**: Inject content script into YouTube pages
- **host_permissions**:
  - `https://www.youtube.com/*`: Access YouTube pages
  - `http://localhost:8000/*`: Call your local API

## 🚀 Development

### Making Changes

1. Edit the extension files as needed
2. Go to `chrome://extensions/`
3. Click the **refresh icon** (🔄) on the Happy Scroll AI extension
4. Reload YouTube page to see changes

### Testing

1. Open a YouTube Short
2. Check Console for logs
3. Verify API calls in Network tab
4. Test with both safe and unsafe videos

## 📝 API Response Format

The extension expects this JSON response from your API:

```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "is_safe": false,
  "reasons": "Inappropriate content detected"
}
```

## 🔄 Updates

To update the extension:
1. Make changes to the files
2. Increment version in `manifest.json`
3. Go to `chrome://extensions/`
4. Click refresh on the extension

## ⚠️ Important Notes

- Extension only works on **YouTube Shorts** (`/shorts/` URLs)
- Requires **active internet connection**
- Requires **running API server** on localhost:8000
- Uses **2-second delay** to ensure page is loaded
- Automatically detects URL changes (SPA navigation)

## 🐛 Troubleshooting

### Extension Not Loading
1. Check all files are in the same folder
2. Verify `manifest.json` is valid JSON
3. Check Chrome DevTools for errors

### API Calls Failing
1. Verify API is running: `curl http://localhost:8000/docs`
2. Test endpoint manually with video URL
3. Check CORS headers are set correctly

### Videos Playing Despite Being Unsafe
1. Check API response in Console
2. Verify `is_safe` field is `false`
3. Check if Next button selector is correct

## 📞 Support

If you encounter issues:
1. Check console logs (F12)
2. Verify API is responding
3. Test with a known unsafe video
4. Review CORS configuration

## 📄 License

This extension is part of the Happy Scroll AI project.

---

**Happy Safe Scrolling! 🎉**
