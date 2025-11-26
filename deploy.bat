@echo off
REM HappyScroll API - Cloud Run Deployment Script (Windows)
REM This script deploys the FastAPI application to Google Cloud Run

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_ID=%GCP_PROJECT_ID%
if "%PROJECT_ID%"=="" set PROJECT_ID=your-project-id
set REGION=us-central1
set SERVICE_NAME=happy-scroll-service
set REPOSITORY=happy-scroll-api
set IMAGE_NAME=happyscroll-api

echo.
echo 🚀 Deploying HappyScroll API to Google Cloud Run
echo ================================================
echo Project ID: %PROJECT_ID%
echo Region: %REGION%
echo Service Name: %SERVICE_NAME%
echo.

REM Step 1: Check authentication
echo 📝 Step 1: Checking authentication...
gcloud auth list --filter=status:ACTIVE --format="value(account)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Not authenticated. Please run: gcloud auth login
    exit /b 1
)
echo ✅ Authenticated

REM Step 2: Set project
echo.
echo 📝 Step 2: Setting project...
gcloud config set project %PROJECT_ID%

REM Step 3: Build Docker image
echo.
echo 📝 Step 3: Building Docker image...
docker build -t %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPOSITORY%/%IMAGE_NAME%:latest .
if errorlevel 1 (
    echo ❌ Docker build failed
    exit /b 1
)
echo ✅ Docker image built

REM Step 4: Configure Docker for Artifact Registry
echo.
echo 📝 Step 4: Configuring Docker authentication...
gcloud auth configure-docker %REGION%-docker.pkg.dev
echo ✅ Docker configured

REM Step 5: Push image to Artifact Registry
echo.
echo 📝 Step 5: Pushing image to Artifact Registry...
docker push %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPOSITORY%/%IMAGE_NAME%:latest
if errorlevel 1 (
    echo ❌ Docker push failed
    exit /b 1
)
echo ✅ Image pushed

REM Step 6: Deploy to Cloud Run
echo.
echo 📝 Step 6: Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPOSITORY%/%IMAGE_NAME%:latest ^
  --platform=managed ^
  --region=%REGION% ^
  --allow-unauthenticated ^
  --port=8080 ^
  --memory=512Mi ^
  --cpu=1 ^
  --min-instances=0 ^
  --max-instances=10 ^
  --timeout=300 ^
  --set-secrets=YOUTUBE_API_KEY=youtube_api_key:latest,GOOGLE_VISION_KEY=google_vision_key:latest,GEMINI_KEY=gemini_key:latest ^
  --set-env-vars=REDIS_URL=%REDIS_URL%

if errorlevel 1 (
    echo ❌ Deployment failed
    exit /b 1
)

echo.
echo ✅ Deployment complete!
echo.
echo 📊 Getting service URL...
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --platform=managed --region=%REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo.
echo 🎉 Deployment successful!
echo ================================
echo Service URL: %SERVICE_URL%
echo ================================
echo.
echo Test your API with:
echo curl -X POST %SERVICE_URL%/api/happyScroll/v1/verdict ^
echo   -H "Content-Type: application/json" ^
echo   -d "{\"video_url\": \"https://youtube.com/shorts/example\"}"
echo.

endlocal
