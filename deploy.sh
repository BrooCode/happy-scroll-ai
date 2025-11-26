#!/bin/bash

# HappyScroll API - Cloud Run Deployment Script
# This script deploys the FastAPI application to Google Cloud Run

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-your-project-id}"
REGION="us-central1"
SERVICE_NAME="happy-scroll-service"
REPOSITORY="happy-scroll-api"
IMAGE_NAME="happyscroll-api"

echo "🚀 Deploying HappyScroll API to Google Cloud Run"
echo "================================================"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo ""

# Step 1: Authenticate (if needed)
echo "📝 Step 1: Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated. Please run: gcloud auth login"
    exit 1
fi
echo "✅ Authenticated"

# Step 2: Set project
echo ""
echo "📝 Step 2: Setting project..."
gcloud config set project $PROJECT_ID

# Step 3: Build Docker image
echo ""
echo "📝 Step 3: Building Docker image..."
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:latest .
echo "✅ Docker image built"

# Step 4: Configure Docker for Artifact Registry
echo ""
echo "📝 Step 4: Configuring Docker authentication..."
gcloud auth configure-docker $REGION-docker.pkg.dev
echo "✅ Docker configured"

# Step 5: Push image to Artifact Registry
echo ""
echo "📝 Step 5: Pushing image to Artifact Registry..."
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:latest
echo "✅ Image pushed"

# Step 6: Deploy to Cloud Run
echo ""
echo "📝 Step 6: Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --timeout=300 \
  --set-secrets=YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest,GOOGLE_VISION_KEY=GOOGLE_VISION_KEY:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest \
  --set-env-vars=REDIS_URL=$REDIS_URL

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Getting service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --platform=managed \
  --region=$REGION \
  --format='value(status.url)')

echo ""
echo "🎉 Deployment successful!"
echo "================================"
echo "Service URL: $SERVICE_URL"
echo "================================"
echo ""
echo "Test your API with:"
echo "curl -X POST $SERVICE_URL/api/happyScroll/v1/verdict \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"video_url\": \"https://youtube.com/shorts/example\"}'"
