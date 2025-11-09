# Sample API Requests

This file contains sample curl commands and PowerShell examples for testing the API.

## Using curl (if available)

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Moderate Content
```bash
curl -X POST http://localhost:8000/api/moderate \
  -H "Content-Type: application/json" \
  -d '{"content": "This is a test message"}'
```

## Using PowerShell

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get
```

### Moderate Content
```powershell
$body = @{
    content = "This is a test message"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Using a JSON file
```powershell
$body = Get-Content -Path "sample_request.json" -Raw

Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Using Python httpx

```python
import httpx

# Health check
response = httpx.get("http://localhost:8000/api/health")
print(response.json())

# Moderate content
response = httpx.post(
    "http://localhost:8000/api/moderate",
    json={"content": "This is a test message"}
)
print(response.json())
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive API documentation where you can test all endpoints directly in your browser.
