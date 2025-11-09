# HappyScroll Moderation API

AI-powered content moderation backend for the HappyScroll Chrome extension. This API uses OpenAI's moderation endpoint to analyze and filter unsafe content in short-form videos.

## Features

- 🚀 **FastAPI Framework** - Modern, fast web framework with automatic API documentation
- 🤖 **OpenAI Integration** - Uses `omni-moderation-latest` model for content analysis
- 🔒 **CORS Support** - Configured for Chrome extension requests
- 📝 **Type Safety** - Full type hints with Pydantic models
- 📊 **Structured Logging** - Enhanced logging with Loguru
- 🐳 **Docker Support** - Containerized deployment ready
- ✅ **Health Checks** - Built-in health monitoring endpoints

## Project Structure

```
happy-scroll-ai/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Environment configuration
│   │   └── logger.py              # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── moderation_request.py  # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── moderation.py          # API endpoints
│   └── services/
│       ├── __init__.py
│       └── openai_service.py      # OpenAI API integration
├── tests/
│   ├── __init__.py
│   └── test_moderation.py         # Unit tests
├── .env.example                    # Environment variables template
├── .gitignore
├── Dockerfile
├── Makefile
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.11+
- OpenAI API key
- pip or Docker

## Quick Start

### 1. Clone and Setup

```bash
cd happy-scroll-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
copy .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
APP_ENV=dev
PORT=8000
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

Or use the Makefile:
```bash
make dev
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Usage

### Moderate Content

**Endpoint**: `POST /api/moderate`

**Request**:
```json
{
  "content": "Text content to moderate"
}
```

**Response**:
```json
{
  "safe": false,
  "categories": ["violence", "hate"],
  "category_scores": {
    "violence": 0.95,
    "hate": 0.78,
    "sexual": 0.01
  }
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
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `APP_ENV`: `prod`
5. **Deploy**

### Deploy to Railway

1. **Create New Project** on [Railway](https://railway.app)
2. **Deploy from GitHub**
3. **Add Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `APP_ENV`: `prod`
   - `PORT`: `8000`
4. **Railway will auto-detect** the Dockerfile and deploy

### Environment Variables for Production

```env
OPENAI_API_KEY=sk-your-production-key
APP_ENV=prod
PORT=8000
```

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
- `openai` - OpenAI API client
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

1. **ModuleNotFoundError: No module named 'pydantic_settings'**
   ```bash
   pip install pydantic-settings
   ```

2. **OpenAI API Key Error**
   - Verify `.env` file exists with correct `OPENAI_API_KEY`
   - Ensure key starts with `sk-`

3. **Port Already in Use**
   ```bash
   # Change PORT in .env or run on different port
   uvicorn app.main:app --port 8001
   ```

## Security Notes

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- In production, use proper secrets management
- Implement rate limiting for public APIs
- Keep dependencies updated

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review [OpenAI API docs](https://platform.openai.com/docs/)

---

Built with ❤️ for HappyScroll Chrome Extension