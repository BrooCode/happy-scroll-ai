# 🛡️ Rate Limiting Implementation

## Overview

To protect API costs and manage the demo nature of this project, we've implemented a **two-layer rate limiting system**:

1. **Client-Side (Chrome Extension)**: 8 videos per user per day
2. **Server-Side (FastAPI Backend)**: 100 total requests per day across all users

---

## 🎯 Why Rate Limiting?

This is a **demo project** using paid services:
- **Google Cloud Run** - Pay-per-request serverless hosting
- **Gemini AI API** - AI content analysis (paid)
- **Google Vision API** - Image moderation (paid)
- **YouTube Data API** - Video metadata (quota limits)

Rate limiting prevents unexpected costs while allowing users to test functionality.

---

## 📊 Client-Side Limit (Chrome Extension)

### Configuration
- **Limit**: 8 videos per day per user
- **Reset**: Midnight local time
- **Storage**: Chrome local storage (`chrome.storage.local`)

### Features
- ✅ Friendly user notification when limit reached
- ✅ Daily automatic counter reset
- ✅ Visible usage tracking in console
- ✅ Graceful degradation (stops checking, doesn't break)
- ✅ Beautiful animated banner notification

### How It Works

```javascript
// Checks limit before each API call
const limitCheck = await checkVideoLimit();

if (!limitCheck.allowed) {
  showLimitMessage(); // Shows banner notification
  return null; // Skips API call
}

// Makes API call and increments counter
const result = await checkVideoSafety(videoId);
await incrementVideoCount();
```

### User Experience

When limit is reached, users see an animated banner:

```
⚠️

Happy Scroll AI - Daily Limit Reached

You've checked 8 videos today.
Come back tomorrow for more safe browsing! 🚀

This is a demo project with limited free API usage.
```

The banner:
- Slides down from the top with animation
- Displays for 6 seconds
- Fades out gracefully
- Uses purple gradient matching the brand

### Console Logs

Users can track their usage in browser console (F12):

```
[Happy Scroll AI] 🔍 Checking video safety (1/8)...
[Happy Scroll AI] 📈 Videos checked today: 1/8
...
[Happy Scroll AI] ⚠️ Daily limit reached (8/8 videos)
```

---

## 🔒 Server-Side Limit (FastAPI Backend)

### Configuration
- **Limit**: 100 requests per day (global across all users)
- **Reset**: Midnight server time (UTC)
- **Storage**: In-memory (resets on server restart)

### Features
- ✅ Global protection across all users
- ✅ HTTP 429 (Too Many Requests) response
- ✅ Detailed error message with info
- ✅ Automatic daily reset
- ✅ Logging for monitoring

### How It Works

```python
# Checks global limit before processing
limit_info = check_global_limit()

if GLOBAL_REQUEST_COUNT >= GLOBAL_DAILY_LIMIT:
    raise HTTPException(
        status_code=429,
        detail={
            "error": "Daily limit exceeded",
            "message": "Demo API has reached its daily limit.",
            "requests_today": GLOBAL_REQUEST_COUNT,
            "limit": GLOBAL_DAILY_LIMIT
        }
    )
```

### API Response (429 Error)

When the global limit is reached:

```json
{
  "detail": {
    "error": "Daily limit exceeded",
    "message": "Demo API has reached its daily limit. Please try again tomorrow!",
    "info": "This is a demo project with limited free tier usage to manage costs.",
    "limit": 100,
    "requests_today": 100,
    "note": "For unlimited usage, please deploy your own instance using the GitHub repository."
  }
}
```

### Server Logs

```
📊 Global requests today: 45/100
INFO: HappyScroll Verdict Request: https://www.youtube.com/watch?v=...
INFO: 📊 Rate Limit: 45/100 (55 remaining)
...
⚠️ Global daily limit reached: 100/100
```

---

## 📈 Usage Tracking

### Extension Console Logs

**Normal usage:**
```
[Happy Scroll AI] Extension initialized
[Happy Scroll AI] 📊 Rate limit: 8 videos per day
[Happy Scroll AI] 🔍 Checking video safety (1/8)...
[Happy Scroll AI] 📈 Videos checked today: 1/8
[Happy Scroll AI] ✅ Video is SAFE - Continuing playback
```

**Limit reached:**
```
[Happy Scroll AI] ⚠️ Daily limit reached (8/8 videos)
[Happy Scroll AI] ⚠️ Skipping check - rate limit or error
```

### Backend Logs

**Normal usage:**
```
🔄 Global rate limit reset for new day: 2024-11-29
📊 Global requests today: 1/100
================================================================================
HappyScroll Verdict Request: https://www.youtube.com/watch?v=dQw4w9WgXcQ
📊 Rate Limit: 1/100 (99 remaining)
================================================================================
```

**Limit reached:**
```
⚠️ Global daily limit reached: 100/100
```

---

## 🔧 Adjusting Limits

### Extension Limit

Edit `Happy Scroll AI/content.js`:

```javascript
// Line 19
const MAX_VIDEOS_PER_DAY = 8; // Change this number
```

### API Limit

Edit `app/routes/happyscroll_verdict.py`:

```python
# Line 29
GLOBAL_DAILY_LIMIT = 100  # Change this number
```

### Redeploy After Changes

**Extension:**
1. Update `content.js`
2. Reload extension in Chrome (`chrome://extensions/`)
3. Test on YouTube Shorts

**Backend:**
1. Update `happyscroll_verdict.py`
2. Commit and push to GitHub
3. GitHub Actions will auto-deploy to Cloud Run
4. Or manually: `./deploy.sh` (Linux/Mac) or `deploy.bat` (Windows)

---

## 🚀 For Production Use

If you want unlimited usage, you have options:

### Option 1: Remove Client Limit

```javascript
// Comment out the limit check in content.js
async function checkVideoSafety(videoId) {
  // const limitCheck = await checkVideoLimit();
  // if (!limitCheck.allowed) {
  //   showLimitMessage();
  //   return null;
  // }
  
  // Rest of the code...
}
```

### Option 2: Remove API Limit

```python
# Comment out the limit check in happyscroll_verdict.py
async def get_video_verdict(request: HappyScrollVerdictRequest):
    # limit_info = check_global_limit()
    
    # Rest of the code...
```

### Option 3: Deploy Your Own Instance

1. **Fork/Clone** the repository
2. **Set up** your own Google Cloud project
3. **Create** your own API keys:
   - YouTube Data API
   - Google Cloud Vision API
   - Gemini AI API
4. **Deploy** with your own Cloud Run service
5. **Configure** your own limits based on your budget

**Estimated monthly costs** (no limits):
- Light usage (100 requests/day): ~$15-25/month
- Medium usage (500 requests/day): ~$75-125/month
- Heavy usage (2000 requests/day): ~$300-500/month

---

## 📊 Cost Estimates (Current Limits)

### Daily Costs (100 requests/day)
- **Gemini API**: ~$0.10 - $0.20
- **Google Vision API**: ~$0.15 - $0.30  
- **Cloud Run**: ~$0.01 - $0.05
- **Redis Cloud**: Free tier
- **YouTube Data API**: Free (within quota)
- **Total**: ~$0.26 - $0.55 per day

### Monthly Costs
- **Estimated**: $7.80 - $16.50 per month
- **Status**: ✅ Well within free tier for demonstration

---

## ✅ Testing the Limits

### Test Extension Limit

1. **Open** YouTube Shorts (`youtube.com/shorts`)
2. **Open** DevTools Console (`F12`)
3. **Watch** 8 different Shorts (extension will check each)
4. **On the 9th video**, you should see:
   - Banner notification on screen
   - Console log: `⚠️ Daily limit reached`
5. **Wait until tomorrow** or manually reset:
   ```javascript
   // In console:
   chrome.storage.local.clear()
   ```

### Test API Limit

Make 100+ requests using curl:

```bash
# Linux/Mac
for i in {1..101}; do
  curl -X POST 'https://happy-scroll-service-zjehvyppna-uc.a.run.app/api/happyScroll/v1/verdict' \
    -H 'Content-Type: application/json' \
    -d '{"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
    -w "\nStatus: %{http_code}\n"
done
```

```powershell
# Windows PowerShell
1..101 | ForEach-Object {
  $response = Invoke-WebRequest -Uri 'https://happy-scroll-service-zjehvyppna-uc.a.run.app/api/happyScroll/v1/verdict' `
    -Method POST `
    -ContentType 'application/json' `
    -Body '{"video_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' `
    -UseBasicParsing
  Write-Host "Request $_ : Status $($response.StatusCode)"
}
```

Request #101 should return **HTTP 429** (Too Many Requests).

---

## 🎯 Best Practices

### ✅ DO

- **Monitor usage** in Google Cloud Console regularly
- **Check logs** for rate limit patterns
- **Adjust limits** based on actual costs and usage
- **Document changes** when modifying limits
- **Communicate limits** clearly to users (README, UI, etc.)
- **Set alerts** in Google Cloud for billing thresholds

### ❌ DON'T

- **Remove limits** without cost monitoring
- **Set limits too low** for meaningful testing
- **Ignore 429 errors** in production
- **Forget to update** both client and server limits
- **Deploy without testing** rate limiting behavior
- **Expose unlimited** API publicly without authentication

---

## 🔍 Monitoring & Debugging

### Check Current Usage (Extension)

Open browser console on YouTube:

```javascript
// Check current count
chrome.storage.local.get(['happyscroll_video_count', 'happyscroll_last_reset'], (data) => {
  console.log('Videos checked:', data.happyscroll_video_count || 0);
  console.log('Last reset:', data.happyscroll_last_reset);
});

// Reset counter manually
chrome.storage.local.set({
  happyscroll_video_count: 0,
  happyscroll_last_reset: new Date().toDateString()
});
```

### Check Current Usage (API)

The API doesn't have a usage endpoint, but you can check logs:

```bash
# View recent logs
gcloud run logs read happy-scroll-service --limit 50 --region us-central1

# Filter for rate limit logs
gcloud run logs read happy-scroll-service --limit 100 --region us-central1 | grep "Rate Limit"
```

### Reset API Counter

The API counter resets automatically at midnight UTC or when the Cloud Run service restarts:

```bash
# Force restart (will reset counter)
gcloud run services update happy-scroll-service --region us-central1
```

---

## 📚 Files Modified

### Chrome Extension
- `Happy Scroll AI/manifest.json` - Added `storage` permission
- `Happy Scroll AI/content.js` - Added rate limiting logic

### Backend API
- `app/routes/happyscroll_verdict.py` - Added global rate limiting

---

## 🆘 Troubleshooting

### Issue: "Extension shows limit but I haven't used it"

**Solution**: Clear extension storage
```javascript
// In browser console:
chrome.storage.local.clear()
```

### Issue: "API returns 429 but I'm the only user"

**Possible causes**:
1. Server restarted and counter didn't reset
2. Cache is serving old requests (doesn't count)
3. Multiple users actually using the API

**Solution**: Wait 24 hours or redeploy service

### Issue: "Rate limit not working"

**Check**:
1. Extension has `storage` permission in manifest
2. Backend has rate limit code deployed
3. Check console/logs for errors

---

## 📞 Support

- **GitHub Issues**: [github.com/BrooCode/happy-scroll-ai/issues](https://github.com/BrooCode/happy-scroll-ai/issues)
- **Documentation**: See README.md for full setup
- **Deployment**: See deployment guides for Cloud Run setup

---

**Last Updated**: November 29, 2024  
**Version**: 1.0.0  
**Rate Limits**: Client 8/day, API 100/day
