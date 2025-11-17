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

### Environment Variables for Production

```env
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json
GOOGLE_CLOUD_PROJECT=your-production-project-id
SAFETY_THRESHOLD=POSSIBLE
APP_ENV=prod
PORT=8000
```

**Security Note**: Never commit service account keys to Git. Use environment variables or secret management services.

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