# HappyScroll Moderation API

AI-powered content moderation backend for the HappyScroll Chrome extension. This API uses **Google Cloud Vision API** with SafeSearch detection to analyze and filter unsafe content in short-form videos.

> **🔄 Recently Migrated**: This project has been migrated from OpenAI to Google Cloud Vision for better performance, reliability, and cost-effectiveness. See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details.

## Features

- 🚀 **FastAPI Framework** - Modern, fast web framework with automatic API documentation
- 🔍 **Google Cloud Vision** - SafeSearch API for image content analysis
- 🎯 **Configurable Safety** - Adjustable safety thresholds for different audiences
- 🔒 **CORS Support** - Configured for Chrome extension requests
- 📝 **Type Safety** - Full type hints with Pydantic models
- 📊 **Structured Logging** - Enhanced logging with Loguru
- 🐳 **Docker Support** - Containerized deployment ready
- ✅ **Health Checks** - Built-in health monitoring endpoints
- 💰 **Free Tier** - 1,000 moderations/month free with Google Cloud

## Project Structure

```
happy-scroll-ai/
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                 # Environment configuration
│   │   └── logger.py                 # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── moderation_request.py     # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── moderation.py             # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── google_vision_service.py  # Google Cloud Vision integration
│       └── google_video_service.py   # Google Video Intelligence (optional)
├── tests/
│   ├── __init__.py
│   └── test_moderation.py            # Unit tests
├── credentials/
│   └── .gitkeep                      # Place service account key here
├── .env.example                       # Environment variables template
├── .gitignore
├── Dockerfile
├── Makefile
├── README.md
├── GOOGLE_CLOUD_SETUP.md              # Setup guide for Google Cloud
├── MIGRATION_GUIDE.md                 # Migration from OpenAI guide
├── requirements.txt
└── test_google_vision.py              # Test script for Google Cloud
```

## Prerequisites

- Python 3.11+
- Google Cloud account with Vision API enabled
- Service account JSON key
- pip or Docker

## Quick Start

### 1. Setup Google Cloud

⚠️ **Important**: Before running the API, you must set up Google Cloud Vision API.

📖 **Detailed instructions**: See [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)

**Quick steps**:
1. Create Google Cloud project
2. Enable Vision API
3. Create service account & download JSON key
4. Place key in `credentials/service-account-key.json`

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and configure:

```powershell
copy .env.example .env
```

Edit `.env`:
```env
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=d:\happy-scroll-ai\credentials\service-account-key.json
GOOGLE_CLOUD_PROJECT=your-project-id-here

# Safety Threshold (UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY)
SAFETY_THRESHOLD=POSSIBLE

# Application
APP_ENV=dev
PORT=8000
```

### 5. Test Google Cloud Setup

```powershell
python test_google_vision.py
```

This will verify your credentials and test the Vision API.

### 6. Run the Application

```powershell
uvicorn app.main:app --reload
```

Or use the Makefile:
```powershell
make dev
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc

## API Usage

### Moderate Image Content

**Endpoint**: `POST /api/moderate`

**Request**:
```json
{
  "image_url": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg"
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

### Example: Test with PowerShell

```powershell
$body = @{
    image_url = "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Moderate Video (Optional)

**Endpoint**: `POST /api/moderate/video`

**Note**: Video analysis is slow (1-5 minutes) and requires videos in Google Cloud Storage.

**Request**:
```json
{
  "video_uri": "gs://your-bucket/video.mp4"
}
```

### Health Check

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "HappyScroll Moderation API",
  "version": "1.0.0"
}
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Or using Make:
```bash
make test
```

## Docker Deployment

### Build Image

```bash
docker build -t happyscroll-api:latest .
```

Or:
```bash
make docker-build
```

### Run Container

```bash
docker run -p 8000:8000 --env-file .env happyscroll-api:latest
```

Or:
```bash
make docker-run
```

## Cloud Deployment

### 🚀 Deploy to Google Cloud Run (Recommended)

Google Cloud Run is the recommended production deployment platform for this API. It offers:
- ✅ **Serverless** - Pay only when your API is used (scale to zero)
- ✅ **Auto-scaling** - Handles traffic spikes automatically
- ✅ **Native Integration** - Works seamlessly with Google Cloud Vision API
- ✅ **Secret Manager** - Secure API key storage
- ✅ **Fast Cold Starts** - Optimized Docker image
- ✅ **Free Tier** - 2 million requests/month free

#### Prerequisites

Before deploying, ensure you have:

1. **Google Cloud Project** with billing enabled
2. **Service Account** with the following roles:
   - Cloud Run Admin
   - Artifact Registry Writer
   - Cloud Build Editor
   - Service Account User
   - Secret Manager Secret Accessor
3. **APIs Enabled**:
   - Cloud Run API
   - Artifact Registry API
   - Cloud Build API
   - Secret Manager API
   - Cloud Vision API
4. **Artifact Registry Repository** created:
   ```bash
   gcloud artifacts repositories create happy-scroll-api \
     --repository-format=docker \
     --location=us-central1 \
     --description="HappyScroll API Docker images"
   ```

#### Setup Secrets in Secret Manager

Store your API keys securely in Google Cloud Secret Manager:

```bash
# Store YouTube API Key
echo -n "your-youtube-api-key" | gcloud secrets create youtube_api_key \
  --data-file=- \
  --replication-policy="automatic"

# Store Google Vision API Key (or use service account)
echo -n "your-google-vision-key" | gcloud secrets create google_vision_key \
  --data-file=- \
  --replication-policy="automatic"

# Store Gemini API Key
echo -n "your-gemini-api-key" | gcloud secrets create gemini_key \
  --data-file=- \
  --replication-policy="automatic"
```

#### Option 1: Automated Deployment with GitHub Actions

**1. Add GitHub Secrets**

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

- `GCP_PROJECT_ID`: Your Google Cloud project ID
- `GCP_SA_KEY`: Service account JSON key (entire content)
- `REDIS_URL`: Your Redis connection URL (if using external Redis)

**2. Push to Main Branch**

The GitHub Actions workflow (`.github/workflows/deploy.yaml`) will automatically:
- Build the Docker image
- Push to Artifact Registry
- Deploy to Cloud Run
- Configure secrets from Secret Manager

```bash
git add .
git commit -m "Deploy to Cloud Run"
git push origin main
```

**3. Monitor Deployment**

Check the Actions tab in your GitHub repository to monitor the deployment progress.

#### Option 2: Manual Deployment

**For Windows (PowerShell)**:

```powershell
# Set environment variables
$env:GCP_PROJECT_ID="your-project-id"
$env:REDIS_URL="your-redis-url"

# Run deployment script
.\deploy.bat
```

**For Linux/Mac (Bash)**:

```bash
# Set environment variables
export GCP_PROJECT_ID="your-project-id"
export REDIS_URL="your-redis-url"

# Make script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

**Or use gcloud CLI directly**:

```bash
# 1. Authenticate
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Build and push Docker image
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/happy-scroll-api/happyscroll-api:latest .
gcloud auth configure-docker us-central1-docker.pkg.dev
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/happy-scroll-api/happyscroll-api:latest

# 4. Deploy to Cloud Run
gcloud run deploy happy-scroll-service \
  --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/happy-scroll-api/happyscroll-api:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --timeout=300 \
  --set-secrets=YOUTUBE_API_KEY=youtube_api_key:latest,GOOGLE_VISION_KEY=google_vision_key:latest,GEMINI_KEY=gemini_key:latest \
  --set-env-vars=REDIS_URL=YOUR_REDIS_URL
```

#### Testing Your Deployment

After deployment, test your API:

```powershell
# Get your service URL
$SERVICE_URL = gcloud run services describe happy-scroll-service `
  --platform=managed `
  --region=us-central1 `
  --format="value(status.url)"

# Test the health endpoint
Invoke-RestMethod -Uri "$SERVICE_URL/api/health"

# Test the verdict endpoint
$body = @{
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