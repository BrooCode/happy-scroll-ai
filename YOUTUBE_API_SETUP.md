# YouTube API Integration Requirements

## Additional Dependencies Needed

Add to `requirements.txt`:
```
google-api-python-client==2.108.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.0
httpx==0.27.0
```

Install with:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib httpx
```

## Environment Variables

Add to `.env`:
```
YOUTUBE_API_KEY=your-youtube-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here  # (already configured)
```

## Get YouTube API Key

1. Go to: https://console.cloud.google.com/
2. Create or select a project
3. Enable YouTube Data API v3
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key to your `.env` file
