# 🚀 Happy Scroll AI# HappyScroll Moderation API



**AI-powered YouTube Shorts content moderation for safer browsing.**AI-powered content moderation backend for the HappyScroll Chrome extension. This API uses **Google Cloud Vision API** with SafeSearch detection to analyze and filter unsafe content in short-form videos.



Automatically analyzes and filters unsafe YouTube Shorts content using advanced AI and computer vision, protecting users from inappropriate videos.> **🔄 Recently Migrated**: This project has been migrated from OpenAI to Google Cloud Vision for better performance, reliability, and cost-effectiveness. See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details.



[![Deploy](https://img.shields.io/badge/Deploy-Google%20Cloud%20Run-4285F4?logo=google-cloud)](https://cloud.google.com/run)## Features

[![API](https://img.shields.io/badge/API-Live-success)](https://happy-scroll-service-zjehvyppna-uc.a.run.app)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)- 🚀 **FastAPI Framework** - Modern, fast web framework with automatic API documentation

- 🔍 **Google Cloud Vision** - SafeSearch API for image content analysis

---- 🎯 **Configurable Safety** - Adjustable safety thresholds for different audiences

- 🔒 **CORS Support** - Configured for Chrome extension requests

## 📋 Overview- 📝 **Type Safety** - Full type hints with Pydantic models

- 📊 **Structured Logging** - Enhanced logging with Loguru

**Happy Scroll AI** is a complete content moderation system consisting of:- 🐳 **Docker Support** - Containerized deployment ready

- ✅ **Health Checks** - Built-in health monitoring endpoints

1. **FastAPI Backend** - Deployed on Google Cloud Run- 💰 **Free Tier** - 1,000 moderations/month free with Google Cloud

2. **Chrome Extension** - Auto-skips unsafe YouTube Shorts

3. **AI Analysis** - Multi-layer safety checks using Gemini AI & Google Vision## Project Structure



**Live Demo:** https://broocode.github.io/happy-scroll-ai/  ```

**API Endpoint:** https://happy-scroll-service-zjehvyppna-uc.a.run.apphappy-scroll-ai/

├── app/

---│   ├── __init__.py

│   ├── main.py                       # FastAPI application entry point

## 🛠️ Technology Stack│   ├── core/

│   │   ├── __init__.py

### **Backend Services**│   │   ├── config.py                 # Environment configuration

| Service | Purpose | Provider |│   │   └── logger.py                 # Logging setup

|---------|---------|----------|│   ├── models/

| **Google Cloud Run** | Serverless API hosting | Google Cloud |│   │   ├── __init__.py

| **Gemini AI API** | Video transcript analysis | Google AI |│   │   └── moderation_request.py     # Pydantic models

| **Google Vision API** | Thumbnail safety detection | Google Cloud |│   ├── routes/

| **YouTube Data API v3** | Video metadata & transcripts | Google Cloud |│   │   ├── __init__.py

| **Redis Cloud** | Response caching (7-day TTL) | Redis Labs |│   │   └── moderation.py             # API endpoints

| **Secret Manager** | Secure API key storage | Google Cloud |│   └── services/

| **Artifact Registry** | Docker image storage | Google Cloud |│       ├── __init__.py

| **GitHub Actions** | CI/CD automation | GitHub |│       ├── google_vision_service.py  # Google Cloud Vision integration

│       └── google_video_service.py   # Google Video Intelligence (optional)

### **Application Stack**├── tests/

- **Framework:** FastAPI 0.109.0 (Python 3.10+)│   ├── __init__.py

- **Validation:** Pydantic 2.7.4│   └── test_moderation.py            # Unit tests

- **Logging:** Loguru├── credentials/

- **Deployment:** Docker + Cloud Run│   └── .gitkeep                      # Place service account key here

- **Cache:** Redis 5.0.1├── .env.example                       # Environment variables template

├── .gitignore

### **Chrome Extension**├── Dockerfile

- **Manifest:** V3├── Makefile

- **Storage:** chrome.storage.local├── README.md

- **Permissions:** activeTab, scripting, storage├── GOOGLE_CLOUD_SETUP.md              # Setup guide for Google Cloud

├── MIGRATION_GUIDE.md                 # Migration from OpenAI guide

---├── requirements.txt

└── test_google_vision.py              # Test script for Google Cloud

## ✨ Features```



### **🔍 Multi-Layer Analysis**## Prerequisites

- ✅ **Transcript Analysis** - AI checks video captions against 12 strict safety rules

- ✅ **Thumbnail Moderation** - Computer vision detects inappropriate imagery- Python 3.11+

- ✅ **Parallel Processing** - Both checks run simultaneously (~15-20s)- Google Cloud account with Vision API enabled

- ✅ **Smart Caching** - 7-day cache for instant responses (<1s)- Service account JSON key

- pip or Docker

### **🛡️ Safety Features**

- ✅ Strict Indian parenting norms compliance## Quick Start

- ✅ Filters: violence, adult content, profanity, dangerous acts

- ✅ Automatic video skipping in Chrome extension### 1. Setup Google Cloud

- ✅ Real-time console logging for transparency

⚠️ **Important**: Before running the API, you must set up Google Cloud Vision API.

### **⚡ Performance**

- ✅ **Cached Videos:** <1 second (instant)📖 **Detailed instructions**: See [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)

- ✅ **New Videos:** 15-25 seconds (parallel analysis)

- ✅ **Cache Hit Rate:** 60-80%**Quick steps**:

- ✅ **Uptime:** 99.9% (Cloud Run)1. Create Google Cloud project

2. Enable Vision API

### **📊 Rate Limiting**3. Create service account & download JSON key

- **Extension:** 8 videos per user per day4. Place key in `credentials/service-account-key.json`

- **API:** 150 NEW analyses per day (cached videos excluded)

- **Cost Protection:** Smart caching reduces API costs by 70%### 2. Create Virtual Environment



---```powershell

python -m venv venv

## 🚀 Quick Start.\venv\Scripts\activate  # Windows PowerShell

```

### **1. Prerequisites**

### 3. Install Dependencies

- Python 3.10+

- Google Cloud account```powershell

- Redis Cloud account (free tier)pip install -r requirements.txt

- GitHub account (for deployment)```



### **2. Clone Repository**### 4. Configure Environment



```bashCopy `.env.example` to `.env` and configure:

git clone https://github.com/BrooCode/happy-scroll-ai.git

cd happy-scroll-ai```powershell

```copy .env.example .env

```

### **3. Google Cloud Setup**

Edit `.env`:

```bash```env

# Create project# Google Cloud Configuration

gcloud projects create happyscroll-YOUR-IDGOOGLE_APPLICATION_CREDENTIALS=d:\happy-scroll-ai\credentials\service-account-key.json

GOOGLE_CLOUD_PROJECT=your-project-id-here

# Enable APIs

gcloud services enable run.googleapis.com# Safety Threshold (UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY)

gcloud services enable artifactregistry.googleapis.comSAFETY_THRESHOLD=POSSIBLE

gcloud services enable secretmanager.googleapis.com

gcloud services enable vision.googleapis.com# Application

gcloud services enable youtube.googleapis.comAPP_ENV=dev

```PORT=8000

```

### **4. Set Up API Keys**

### 5. Test Google Cloud Setup

Create secrets in Google Cloud Secret Manager:

```powershell

```bashpython test_google_vision.py

# YouTube Data API key```

echo -n "YOUR_YOUTUBE_KEY" | gcloud secrets create YOUTUBE_API_KEY --data-file=-

This will verify your credentials and test the Vision API.

# Google Vision API key

echo -n "YOUR_VISION_KEY" | gcloud secrets create GOOGLE_VISION_KEY --data-file=-### 6. Run the Application



# Gemini AI API key```powershell

echo -n "YOUR_GEMINI_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=-uvicorn app.main:app --reload

``````



### **5. Deploy to Cloud Run**Or use the Makefile:

```powershell

```bashmake dev

# Using GitHub Actions (Recommended)```

git push origin main

The API will be available at:

# Or deploy manually- **API**: http://localhost:8000

gcloud run deploy happy-scroll-service \- **Docs**: http://localhost:8000/docs (Interactive API documentation)

  --source . \- **ReDoc**: http://localhost:8000/redoc

  --region us-central1 \

  --allow-unauthenticated \## API Usage

  --set-secrets=YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest,GOOGLE_VISION_KEY=GOOGLE_VISION_KEY:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest

```### Moderate Image Content



### **6. Install Chrome Extension****Endpoint**: `POST /api/moderate`



1. Open Chrome → `chrome://extensions/`**Request**:

2. Enable "Developer mode"```json

3. Click "Load unpacked"{

4. Select `Happy Scroll AI/` folder  "image_url": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"

5. Navigate to YouTube Shorts - extension auto-activates!}

```

---

**Response**:

## 📡 API Documentation```json

{

### **Main Endpoint**  "allowed": true,

  "safe": true,

**`POST /api/happyScroll/v1/verdict`**  "categories": {

    "adult": false,

Analyzes YouTube video for safety using parallel transcript + thumbnail checks.    "violence": false,

    "racy": false,

**Request:**    "medical": false,

```json    "spoof": false

{  },

  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"  "likelihood_scores": {

}    "adult": "VERY_UNLIKELY",

```    "violence": "UNLIKELY",

    "racy": "VERY_UNLIKELY",

**Response:**    "medical": "UNLIKELY",

```json    "spoof": "VERY_UNLIKELY"

{  },

  "video_id": "VIDEO_ID",  "threshold": "POSSIBLE",

  "video_title": "Video Title",  "service": "google_cloud_vision"

  "channel_title": "Channel Name",}

  "is_safe": true,```

  "overall_reason": "Video passed all safety checks",

  "transcript_analysis": {### Example: Test with PowerShell

    "is_safe": true,

    "reason": "Content is appropriate"```powershell

  },$body = @{

  "thumbnail_analysis": {    image_url = "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"

    "is_safe": true,} | ConvertTo-Json

    "reason": "No inappropriate content detected"

  },Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" `

  "cached": false,    -Method Post `

  "processing_time": 18.5    -ContentType "application/json" `

}    -Body $body

``````



### **Other Endpoints**### Moderate Video (Optional)



- **Health Check:** `GET /health`**Endpoint**: `POST /api/moderate/video`

- **Cache Stats:** `GET /api/happyScroll/v1/cache/stats`

- **API Docs:** `GET /docs` (Swagger UI)**Note**: Video analysis is slow (1-5 minutes) and requires videos in Google Cloud Storage.



**Live API:** https://happy-scroll-service-zjehvyppna-uc.a.run.app/docs**Request**:

```json

---{

  "video_uri": "gs://your-bucket/video.mp4"

## 🏗️ Architecture}

```

```

┌─────────────────┐### Health Check

│  User Browser   │

│ YouTube Shorts  │**Endpoint**: `GET /api/health`

└────────┬────────┘

         │**Response**:

         ├─────────────────────────────────┐```json

         │                                 │{

┌────────▼────────┐              ┌────────▼─────────┐  "status": "healthy",

│ Chrome Extension│              │   GitHub Pages   │  "service": "HappyScroll Moderation API",

│  (Rate Limited) │              │   Landing Page   │  "version": "1.0.0"

│   8 videos/day  │              └──────────────────┘}

└────────┬────────┘```

         │ HTTPS POST

         │## Testing

┌────────▼─────────────────────────────────┐

│       Google Cloud Run                   │Run the test suite:

│   FastAPI Backend (Python)               │

│   • Rate Limiting: 150 NEW/day           │```bash

│   • Auto-scaling: 0-100 instances        │pytest tests/ -v

│   • Region: us-central1                  │```

└────┬─────────────┬──────────┬────────────┘

     │             │          │Or using Make:

     │             │          │```bash

┌────▼──────┐ ┌────▼─────┐ ┌─▼────────────┐make test

│ Redis     │ │ Gemini   │ │ Google Cloud │```

│ Cloud     │ │ AI API   │ │ Vision API   │

│ (Cache)   │ │          │ │              │## Docker Deployment

└───────────┘ └──────────┘ └──────────────┘

     │             │               │### Build Image

     └─────────────┴───────────────┘

                   │```bash

          ┌────────▼──────────┐docker build -t happyscroll-api:latest .

          │  YouTube Data API │```

          │  (Transcripts)    │

          └───────────────────┘Or:

``````bash

make docker-build

---```



## 💰 Cost Breakdown### Run Container



### **Monthly Costs (Demo Usage)**```bash

docker run -p 8000:8000 --env-file .env happyscroll-api:latest

| Service | Usage | Cost |```

|---------|-------|------|

| **Cloud Run** | 150 requests/day | ~$1-2 |Or:

| **Gemini AI** | 150 analyses/day | ~$3-5 |```bash

| **Google Vision** | 150 analyses/day | ~$4-6 |make docker-run

| **YouTube API** | 150 requests/day | FREE (quota) |```

| **Redis Cloud** | Free tier | $0 |

| **Secret Manager** | 3 secrets | <$1 |## Cloud Deployment

| **Artifact Registry** | 1 image | <$1 |

| **GitHub Actions** | CI/CD | FREE |### 🚀 Deploy to Google Cloud Run (Recommended)

| **GitHub Pages** | Static site | FREE |

| **TOTAL** | | **~$10-15/month** |Google Cloud Run is the recommended production deployment platform for this API. It offers:

- ✅ **Serverless** - Pay only when your API is used (scale to zero)

**With Cache Optimization (70% hit rate):**- ✅ **Auto-scaling** - Handles traffic spikes automatically

- Effective capacity: ~500 checks/day- ✅ **Native Integration** - Works seamlessly with Google Cloud Vision API

- Actual cost: Same (~$10-15)- ✅ **Secret Manager** - Secure API key storage

- Cost per check: $0.001 (vs $0.003 without cache)- ✅ **Fast Cold Starts** - Optimized Docker image

- ✅ **Free Tier** - 2 million requests/month free

---

#### Prerequisites

## 📊 Performance Metrics

Before deploying, ensure you have:

| Metric | Value |

|--------|-------|1. **Google Cloud Project** with billing enabled

| **Cold Start** | ~3-5 seconds |2. **Service Account** with the following roles:

| **Warm Response (Cached)** | <1 second |   - Cloud Run Admin

| **Warm Response (New)** | 15-25 seconds |   - Artifact Registry Writer

| **Cache Hit Rate** | 60-80% |   - Cloud Build Editor

| **API Uptime** | 99.9% |   - Service Account User

| **Max Concurrency** | 100 instances |   - Secret Manager Secret Accessor

| **Memory Usage** | ~512MB per instance |3. **APIs Enabled**:

   - Cloud Run API

---   - Artifact Registry API

   - Cloud Build API

## 🛡️ Safety Rules   - Secret Manager API

   - Cloud Vision API

The API enforces **12 strict safety rules** based on Indian parenting norms:4. **Artifact Registry Repository** created:

   ```bash

1. ❌ Violence or physical harm   gcloud artifacts repositories create happy-scroll-api \

2. ❌ Adult or sexual content     --repository-format=docker \

3. ❌ Profanity or vulgar language     --location=us-central1 \

4. ❌ Dangerous challenges/pranks     --description="HappyScroll API Docker images"

5. ❌ Substance abuse   ```

6. ❌ Bullying or harassment

7. ❌ Hate speech or discrimination#### Setup Secrets in Secret Manager

8. ❌ Scary or disturbing content

9. ❌ Inappropriate relationshipsStore your API keys securely in Google Cloud Secret Manager:

10. ❌ Gambling or illegal activities

11. ❌ Misinformation or conspiracy theories```bash

12. ❌ Privacy violations# Store YouTube API Key

echo -n "your-youtube-api-key" | gcloud secrets create youtube_api_key \

---  --data-file=- \

  --replication-policy="automatic"

## 🔧 Configuration

# Store Google Vision API Key (or use service account)

### **Environment Variables**echo -n "your-google-vision-key" | gcloud secrets create google_vision_key \

  --data-file=- \

```env  --replication-policy="automatic"

# API Keys (stored in Secret Manager)

YOUTUBE_API_KEY=your_key_here# Store Gemini API Key

GOOGLE_VISION_KEY=your_key_hereecho -n "your-gemini-api-key" | gcloud secrets create gemini_key \

GEMINI_API_KEY=your_key_here  --data-file=- \

  --replication-policy="automatic"

# Redis Cache```

REDIS_URL=redis://user:pass@host:port

#### Option 1: Automated Deployment with GitHub Actions

# Application

APP_ENV=production**1. Add GitHub Secrets**

PORT=8080

```Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:



### **Rate Limits (Adjustable)**- `GCP_PROJECT_ID`: Your Google Cloud project ID

- `GCP_SA_KEY`: Service account JSON key (entire content)

**Extension:** `Happy Scroll AI/content.js`- `REDIS_URL`: Your Redis connection URL (if using external Redis)

```javascript

const MAX_VIDEOS_PER_DAY = 8;  // Change as needed**2. Push to Main Branch**

```

The GitHub Actions workflow (`.github/workflows/deploy.yaml`) will automatically:

**API:** `app/routes/happyscroll_verdict.py`- Build the Docker image

```python- Push to Artifact Registry

GLOBAL_DAILY_LIMIT = 150  # Change as needed- Deploy to Cloud Run

```- Configure secrets from Secret Manager



---```bash

git add .

## 📖 Documentationgit commit -m "Deploy to Cloud Run"

git push origin main

- **[API Examples](API_EXAMPLES.md)** - Code samples for using the API```

- **[Chrome Extension Setup](CHROME_EXTENSION_SETUP.md)** - Extension installation guide

- **[Chrome Web Store Guide](CHROME_WEB_STORE_GUIDE.md)** - Publishing to Chrome Web Store**3. Monitor Deployment**

- **[Rate Limit Documentation](RATE_LIMIT_DOCUMENTATION.md)** - Detailed rate limiting info

- **[Quickstart Guide](QUICKSTART.md)** - Fast setup for developersCheck the Actions tab in your GitHub repository to monitor the deployment progress.



---#### Option 2: Manual Deployment



## 🧪 Testing**For Windows (PowerShell)**:



### **Test API Locally**```powershell

# Set environment variables

```bash$env:GCP_PROJECT_ID="your-project-id"

# Install dependencies$env:REDIS_URL="your-redis-url"

pip install -r requirements.txt

# Run deployment script

# Run server.\deploy.bat

uvicorn app.main:app --reload```



# Test endpoint**For Linux/Mac (Bash)**:

curl -X POST "http://localhost:8000/api/happyScroll/v1/verdict" \

  -H "Content-Type: application/json" \```bash

  -d '{"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'# Set environment variables

```export GCP_PROJECT_ID="your-project-id"

export REDIS_URL="your-redis-url"

### **Test Chrome Extension**

# Make script executable

1. Load extension in Chromechmod +x deploy.sh

2. Open YouTube Shorts

3. Check console (F12) for logs# Run deployment script

4. Verify unsafe videos are auto-skipped./deploy.sh

```

---

**Or use gcloud CLI directly**:

## 🤝 Contributing

```bash

Contributions welcome! Please:# 1. Authenticate

gcloud auth login

1. Fork the repository

2. Create a feature branch# 2. Set project

3. Make your changesgcloud config set project YOUR_PROJECT_ID

4. Submit a pull request

# 3. Build and push Docker image

---docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/happy-scroll-api/happyscroll-api:latest .

gcloud auth configure-docker us-central1-docker.pkg.dev

## 📄 Licensedocker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/happy-scroll-api/happyscroll-api:latest



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.# 4. Deploy to Cloud Run

gcloud run deploy happy-scroll-service \

---  --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/happy-scroll-api/happyscroll-api:latest \

  --platform=managed \

## 👨‍💻 Author  --region=us-central1 \

  --allow-unauthenticated \

**BrooCode**  --port=8080 \

  --memory=512Mi \

- GitHub: [@BrooCode](https://github.com/BrooCode)  --cpu=1 \

- Project: [happy-scroll-ai](https://github.com/BrooCode/happy-scroll-ai)  --min-instances=0 \

  --max-instances=10 \

---  --timeout=300 \

  --set-secrets=YOUTUBE_API_KEY=youtube_api_key:latest,GOOGLE_VISION_KEY=google_vision_key:latest,GEMINI_KEY=gemini_key:latest \

## 🙏 Acknowledgments  --set-env-vars=REDIS_URL=YOUR_REDIS_URL

```

- **Google Cloud Platform** - Cloud Run, Vision API, Secret Manager

- **Google AI** - Gemini AI for transcript analysis#### Testing Your Deployment

- **Redis Labs** - Free Redis Cloud tier

- **FastAPI** - Modern Python web frameworkAfter deployment, test your API:

- **YouTube** - Data API for video metadata

```powershell

---# Get your service URL

$SERVICE_URL = gcloud run services describe happy-scroll-service `

## 📞 Support  --platform=managed `

  --region=us-central1 `

- **Issues:** [GitHub Issues](https://github.com/BrooCode/happy-scroll-ai/issues)  --format="value(status.url)"

- **Demo:** https://broocode.github.io/happy-scroll-ai/

- **API:** https://happy-scroll-service-zjehvyppna-uc.a.run.app/docs# Test the health endpoint

Invoke-RestMethod -Uri "$SERVICE_URL/api/health"

---

# Test the verdict endpoint

**Made with ❤️ for safer browsing**$body = @{

    video_url = "https://youtube.com/shorts/example"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$SERVICE_URL/api/happyScroll/v1/verdict" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

#### Update Chrome Extension

Update your Chrome extension's `content.js` with the deployed URL:

```javascript
const API_URL = 'https://your-service-url.run.app/api/happyScroll/v1/verdict';
```

#### Monitoring and Logs

**View logs**:
```bash
gcloud run services logs read happy-scroll-service \
  --region=us-central1 \
  --limit=50
```

**View metrics** in Google Cloud Console:
- Go to Cloud Run → happy-scroll-service
- Click on "METRICS" tab
- Monitor requests, latency, CPU, and memory usage

#### Cost Optimization

Cloud Run pricing (as of 2024):
- **Free Tier**: 2 million requests/month
- **CPU**: $0.00002400/vCPU-second
- **Memory**: $0.00000250/GiB-second
- **Requests**: $0.40 per million

**Estimated costs** for typical usage:
- 10,000 requests/month: **FREE** ✨
- 100,000 requests/month: ~$2-5/month
- 1,000,000 requests/month: ~$10-20/month

**Tips to reduce costs**:
- Use `--min-instances=0` to scale to zero when not in use
- Enable CPU allocation only during request processing (default)
- Implement caching (already done with Redis)
- Use appropriate memory limits (512Mi is sufficient)

#### CI/CD Pipeline

The GitHub Actions workflow automatically:
1. ✅ Triggers on push to `main` branch
2. ✅ Authenticates with Google Cloud
3. ✅ Builds multi-stage Docker image
4. ✅ Pushes to Artifact Registry
5. ✅ Deploys to Cloud Run with secrets
6. ✅ Reports deployment URL

**Workflow file**: `.github/workflows/deploy.yaml`

#### Rollback

If you need to rollback to a previous version:

```bash
# List revisions
gcloud run revisions list --service=happy-scroll-service --region=us-central1

# Rollback to specific revision
gcloud run services update-traffic happy-scroll-service \
  --to-revisions=REVISION_NAME=100 \
  --region=us-central1
```

#### Environment Variables in Cloud Run

The deployment automatically configures:
- `PORT`: 8080 (Cloud Run requirement)
- `YOUTUBE_API_KEY`: From Secret Manager (youtube_api_key)
- `GOOGLE_VISION_KEY`: From Secret Manager (google_vision_key)
- `GEMINI_KEY`: From Secret Manager (gemini_key)
- `REDIS_URL`: From environment variable

#### Troubleshooting Deployment

**Issue**: Container fails to start
```bash
# Check logs
gcloud run services logs read happy-scroll-service --region=us-central1 --limit=100
```

**Issue**: Permission denied
```bash
# Grant service account access to secrets
gcloud secrets add-iam-policy-binding youtube_api_key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"
```

**Issue**: Deployment times out
- Increase `--timeout` to 600 seconds
- Check Docker image size (should be < 1GB)
- Verify dependencies in requirements.txt

---

### Deploy to Render

1. **Create New Web Service** on [Render](https://render.com)
2. **Connect your GitHub repository**
3. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Add Environment Variables**:
   - `GOOGLE_APPLICATION_CREDENTIALS`: Upload JSON key as secret file
   - `GOOGLE_CLOUD_PROJECT`: Your project ID
   - `SAFETY_THRESHOLD`: `POSSIBLE`
   - `APP_ENV`: `prod`
5. **Upload service account JSON** as secret file
6. **Deploy**

### Deploy to Railway

1. **Create New Project** on [Railway](https://railway.app)
2. **Deploy from GitHub**
3. **Add Environment Variables**:
   - `GOOGLE_APPLICATION_CREDENTIALS`: `/app/credentials/service-account-key.json`
   - `GOOGLE_CLOUD_PROJECT`: Your project ID
   - `SAFETY_THRESHOLD`: `POSSIBLE`
   - `APP_ENV`: `prod`
   - `PORT`: `8000`
4. **Upload service account JSON** to `/app/credentials/`
5. **Railway will auto-detect** the Dockerfile and deploy

---

### Environment Variables for Production

**Cloud Run** (uses Secret Manager):
```env
# Managed by Secret Manager
YOUTUBE_API_KEY=youtube_api_key:latest
GOOGLE_VISION_KEY=google_vision_key:latest
GEMINI_KEY=gemini_key:latest

# Environment variables
REDIS_URL=your-redis-connection-url
PORT=8080
```

**Other Platforms**:
```env
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json
GOOGLE_CLOUD_PROJECT=your-production-project-id
SAFETY_THRESHOLD=POSSIBLE
APP_ENV=prod
PORT=8000
```

**Security Note**: 
- ✅ Use Secret Manager for sensitive data on Cloud Run
- ✅ Never commit service account keys to Git
- ✅ Use environment variables for configuration
- ✅ Enable VPC for additional network security

## Development

### Available Make Commands

```bash
make help          # Show all commands
make install       # Install dependencies
make run           # Run application
make dev           # Run with auto-reload
make test          # Run tests
make format        # Format code with black
make lint          # Lint code with flake8
make clean         # Clean cache files
make docker-build  # Build Docker image
make docker-run    # Run Docker container
```

### Code Formatting

Format code with Black:
```bash
pip install black
black app/ tests/
```

Or:
```bash
make format
```

### Linting

Lint with flake8:
```bash
pip install flake8
flake8 app/ tests/ --max-line-length=100
```

Or:
```bash
make lint
```

## Project Configuration

### requirements.txt

All dependencies are pinned for reproducible builds:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `google-cloud-vision` - Google Cloud Vision API client
- `google-cloud-videointelligence` - Video analysis (optional)
- `pillow` - Image processing
- `aiohttp` - Async HTTP client for image downloads
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- `loguru` - Enhanced logging
- `pytest` - Testing framework
- `httpx` - HTTP client for tests

### CORS Configuration

The API is configured to accept requests from Chrome extensions. In production, you may want to restrict origins in `app/core/config.py`:

```python
allowed_origins: list[str] = [
    "chrome-extension://*",
    "https://yourdomain.com",
]
```

## Monitoring and Logs

### Development

Logs are output to console with color-coded levels.

### Production

Logs are written to:
- Console (JSON format)
- `logs/app.log` (rotated at 500MB, kept for 10 days)

## Troubleshooting

### Common Issues

1. **"Could not load credentials"**
   - Check `GOOGLE_APPLICATION_CREDENTIALS` path in `.env`
   - Verify JSON key file exists at that path
   - Run `python test_google_vision.py` to diagnose

2. **"Vision API has not been enabled"**
   - Go to https://console.cloud.google.com/apis/library/vision.googleapis.com
   - Click "Enable"
   - Wait 1-2 minutes and try again

3. **"Permission denied"**
   - Verify service account has role: `Cloud Vision AI Service Agent`
   - Check IAM permissions in Google Cloud Console

4. **ModuleNotFoundError: No module named 'google.cloud'**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Port Already in Use**
   ```powershell
   # Change PORT in .env or run on different port
   uvicorn app.main:app --port 8001
   ```

For detailed troubleshooting, see [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md#-troubleshooting).

## Security Notes

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- In production, use proper secrets management
- Implement rate limiting for public APIs
- Keep dependencies updated

## License

MIT License - see LICENSE file for details

## Documentation

- 📖 **[Google Cloud Setup Guide](GOOGLE_CLOUD_SETUP.md)** - Complete setup instructions
- 🔄 **[Migration Guide](MIGRATION_GUIDE.md)** - Migrating from OpenAI to Google Cloud
- 🧪 **[Test Script](test_google_vision.py)** - Verify your setup

## Pricing

**Google Cloud Vision API**:
- **First 1,000 images/month**: FREE ✨
- **1,001 - 5,000,000**: $1.50 per 1,000 images
- **5,000,001+**: $0.60 per 1,000 images

**Example costs**:
- 10,000 moderations = ~$15/month
- 100,000 moderations = ~$150/month

Much more cost-effective than OpenAI for high-volume image moderation!

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review [Google Cloud Vision docs](https://cloud.google.com/vision/docs)
- See [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) for setup help

---

Built with ❤️ for HappyScroll Chrome Extension | Powered by Google Cloud Vision AI