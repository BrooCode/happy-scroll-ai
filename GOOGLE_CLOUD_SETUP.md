# Google Cloud Vision API Setup Guide

## 🚀 Complete Migration from OpenAI to Google Cloud Vision

This guide will help you set up Google Cloud Vision API for the HappyScroll content moderation system.

---

## 📋 Prerequisites

- Google Cloud account
- Python 3.11+
- Basic understanding of Google Cloud Console

---

## 🔧 Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project**:
   - Click "Select a project" → "New Project"
   - Name: `happyscroll-moderation` (or your choice)
   - Click "Create"
3. **Note your Project ID** (you'll need this later)

---

## 🔑 Step 2: Enable Required APIs

1. **Enable Vision API**:
   ```
   https://console.cloud.google.com/apis/library/vision.googleapis.com
   ```
   - Click "Enable"

2. **Enable Video Intelligence API** (optional, for video analysis):
   ```
   https://console.cloud.google.com/apis/library/videointelligence.googleapis.com
   ```
   - Click "Enable"

---

## 🎫 Step 3: Create Service Account & Credentials

1. **Go to IAM & Admin → Service Accounts**:
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts
   ```

2. **Create Service Account**:
   - Click "+ CREATE SERVICE ACCOUNT"
   - Name: `happyscroll-api`
   - Description: "HappyScroll content moderation service"
   - Click "CREATE AND CONTINUE"

3. **Grant Permissions**:
   - Role: `Cloud Vision AI Service Agent`
   - (Optional) Role: `Video Intelligence Service Agent` (for video analysis)
   - Click "CONTINUE" → "DONE"

4. **Create JSON Key**:
   - Click on the service account you just created
   - Go to "KEYS" tab
   - Click "ADD KEY" → "Create new key"
   - Type: **JSON**
   - Click "CREATE"
   - **Save the downloaded JSON file securely**

---

## 📁 Step 4: Configure Your Project

### 1. Place Service Account Key

Save your downloaded JSON key file in your project:

```bash
# Example location:
d:\happy-scroll-ai\credentials\service-account-key.json
```

**⚠️ IMPORTANT**: Never commit this file to Git!

### 2. Update `.env` File

Open `d:\happy-scroll-ai\.env` and update:

```env
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=d:\happy-scroll-ai\credentials\service-account-key.json
GOOGLE_CLOUD_PROJECT=your-project-id-here

# Safety Threshold (UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY)
SAFETY_THRESHOLD=POSSIBLE

# Application Environment
APP_ENV=dev

# Server Configuration
PORT=8000
```

**Replace**:
- `your-project-id-here` with your actual Google Cloud project ID
- Path to your actual service account key file

### 3. Add to `.gitignore`

Make sure your `.gitignore` includes:

```gitignore
# Google Cloud credentials
credentials/
service-account-key.json
*.json
!package.json
```

---

## 📦 Step 5: Install Dependencies

```powershell
# Install new dependencies
python -m pip install -r requirements.txt
```

This installs:
- `google-cloud-vision==3.7.0`
- `google-cloud-videointelligence==2.13.0`
- `pillow==10.2.0`
- `aiohttp==3.9.3`

---

## ✅ Step 6: Verify Setup

### Test 1: Check Credentials

```powershell
python -c "import os; from google.cloud import vision; print('Credentials OK!' if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') else 'No credentials set')"
```

### Test 2: Quick API Test

Create `test_google_vision.py`:

```python
import asyncio
from app.services.google_vision_service import get_vision_service

async def test():
    service = get_vision_service()
    # Test with a safe image
    result = await service.is_safe_content(
        "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Dove_2880p_001.width-1300.jpg"
    )
    print(f"Is safe: {result}")

asyncio.run(test())
```

Run it:
```powershell
python test_google_vision.py
```

---

## 🎯 Step 7: Start Your API

```powershell
python -m uvicorn app.main:app --reload
```

Your API will be available at:
- http://localhost:8000
- http://localhost:8000/docs (Swagger UI)

---

## 📊 API Usage Examples

### Example 1: Moderate YouTube Thumbnail

**Request** (POST `/api/moderate`):
```json
{
  "image_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
}
```

**Response**:
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

### Example 2: PowerShell Test

```powershell
$body = @{
    image_url = "https://example.com/image.jpg"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Example 3: JavaScript (Browser Extension)

```javascript
async function checkContent(imageUrl) {
  const response = await fetch('http://localhost:8000/api/moderate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_url: imageUrl })
  });
  
  const result = await response.json();
  return result.allowed; // true if safe, false if should skip
}

// Usage
const isafe = await checkContent('https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg');
if (!isSafe) {
  // Skip this content
  skipToNextShort();
}
```

---

## 🔧 Safety Threshold Configuration

Adjust sensitivity in `.env`:

| Threshold | Description | Use Case |
|-----------|-------------|----------|
| `VERY_UNLIKELY` | Most permissive | General audiences |
| `UNLIKELY` | Permissive | Teens+ |
| `POSSIBLE` | Balanced (default) | **Recommended for kids** |
| `LIKELY` | Strict | Young children |
| `VERY_LIKELY` | Very strict | Maximum safety |

---

## 💰 Pricing Information

### Google Cloud Vision API Pricing

**SafeSearch Detection**:
- First 1,000 images/month: **FREE**
- 1,001 - 5,000,000: **$1.50 per 1,000 images**
- 5,000,001+: **$0.60 per 1,000 images**

**Example Costs**:
- 10,000 moderations = **$15/month**
- 100,000 moderations = **$150/month**
- Much cheaper than OpenAI for image moderation!

### Video Intelligence API (Optional)

**Explicit Content Detection**:
- $0.10 per minute of video

**Note**: Video analysis is slow (1-5 minutes per video) and expensive. Use only for pre-processing, not real-time filtering.

---

## 🐛 Troubleshooting

### Error: "Could not load credentials"

**Solution**:
1. Check `GOOGLE_APPLICATION_CREDENTIALS` path in `.env`
2. Ensure JSON key file exists at that path
3. Verify file permissions

```powershell
# Check if file exists
Test-Path "d:\happy-scroll-ai\credentials\service-account-key.json"
```

### Error: "API not enabled"

**Solution**:
1. Enable Vision API: https://console.cloud.google.com/apis/library/vision.googleapis.com
2. Wait 1-2 minutes for activation
3. Try again

### Error: "Permission denied"

**Solution**:
1. Go to IAM & Admin → Service Accounts
2. Check your service account has role: `Cloud Vision AI Service Agent`
3. If not, click service account → "Permissions" → "Grant Access" → Add role

### Error: "Quota exceeded"

**Solution**:
1. Check quota: https://console.cloud.google.com/apis/api/vision.googleapis.com/quotas
2. Request quota increase if needed
3. Check billing is enabled

---

## 🔒 Security Best Practices

1. **Never commit service account keys to Git**
   - Add to `.gitignore`
   - Use environment variables

2. **Restrict service account permissions**
   - Only grant Vision API access
   - Don't use owner/editor roles

3. **Use separate keys for dev/prod**
   - Different service accounts
   - Different projects if possible

4. **Rotate keys regularly**
   - Every 90 days recommended
   - Delete old keys

5. **Monitor API usage**
   - Set up billing alerts
   - Review usage logs

---

## 📚 Additional Resources

- **Google Cloud Vision Docs**: https://cloud.google.com/vision/docs
- **SafeSearch Detection**: https://cloud.google.com/vision/docs/detecting-safe-search
- **Video Intelligence**: https://cloud.google.com/video-intelligence/docs
- **Pricing Calculator**: https://cloud.google.com/products/calculator

---

## ✅ Next Steps

1. ✅ Set up Google Cloud project
2. ✅ Enable Vision API
3. ✅ Create service account & download JSON key
4. ✅ Configure `.env` file
5. ✅ Install dependencies
6. ✅ Test the API
7. 🚀 **Start moderating content!**

---

**You're all set! Your HappyScroll API now uses Google Cloud Vision for content moderation.** 🎉
