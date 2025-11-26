# Fix ALL IAM Permissions for Cloud Run Deployment

The deployment is failing because the service account is missing multiple required permissions.

## 🔴 Current Errors

1. ❌ **Artifact Registry**: Permission denied to upload Docker images
2. ❌ **Cloud Run**: Permission denied to deploy services

## 🔧 Complete Solution (One Command!)

### **Open Google Cloud Shell**
Click here: **https://console.cloud.google.com/?cloudshell=true**

### **Run This Single Command Block**

Copy and paste this entire block into Cloud Shell:

```bash
# Set project
gcloud config set project happyscroll-478318

# Create Artifact Registry repository (if not exists)
echo "📦 Creating Artifact Registry repository..."
gcloud artifacts repositories create happy-scroll-api \
  --repository-format=docker \
  --location=us-central1 \
  --description="HappyScroll API Docker images" 2>/dev/null || echo "✓ Repository already exists"

echo ""
echo "🔐 Granting ALL required permissions to service account..."

# Grant Artifact Registry Writer role
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer" \
  --quiet

# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --role="roles/run.admin" \
  --quiet

# Grant Service Account User role
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser" \
  --quiet

# Grant Secret Manager Secret Accessor role
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --quiet

# Grant Cloud Build Editor role (optional but helpful)
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.editor" \
  --quiet

echo ""
echo "✅ All permissions granted successfully!"
echo ""
echo "📋 Verifying permissions..."
gcloud projects get-iam-policy happyscroll-478318 \
  --flatten="bindings[].members" \
  --filter="bindings.members:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --format="table(bindings.role)"

echo ""
echo "🎉 Setup complete! Wait 1-2 minutes, then re-run your GitHub Actions workflow."
```

---

## ✅ Required Roles for Deployment

Your service account needs ALL these roles:
- ❌ **Artifact Registry Writer** - Upload Docker images (MISSING!)
- ❌ **Cloud Run Admin** - Deploy services (MISSING!)
- ❌ **Service Account User** - Use service accounts (MISSING!)
- ❌ **Secret Manager Secret Accessor** - Access secrets (MISSING!)
- ⚠️ **Cloud Build Editor** - Build images (OPTIONAL)

---

## 🚀 After Granting Permissions

1. **Wait 1-2 minutes** for permissions to propagate

2. **Re-run the GitHub Actions workflow**:
   - Go to: https://github.com/BrooCode/happy-scroll-ai/actions
   - Click the failed workflow run
   - Click **"Re-run all jobs"** button (top right)

---

## 🎯 What These Permissions Do

| Role | Purpose | Why Needed |
|------|---------|------------|
| **Artifact Registry Writer** | Push Docker images | Upload built images to registry |
| **Cloud Run Admin** | Deploy services | Create/update Cloud Run services |
| **Service Account User** | Impersonate accounts | Deploy with proper identity |
| **Secret Manager Secret Accessor** | Read secrets | Access API keys from Secret Manager |
| **Cloud Build Editor** | Build images | Optional: Build Docker images in GCP |

---

## � Troubleshooting

**If you still get permission errors:**

1. **Check if secrets exist in Secret Manager**:
```bash
gcloud secrets list --project=happyscroll-478318
```

If missing, create them:
```bash
echo -n "your-youtube-api-key" | gcloud secrets create youtube_api_key --data-file=-
echo -n "your-google-vision-key" | gcloud secrets create google_vision_key --data-file=-
echo -n "your-gemini-api-key" | gcloud secrets create gemini_key --data-file=-
```

2. **Enable required APIs**:
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com --project=happyscroll-478318
```

---

## 🎯 Next Steps

1. ✅ **Open Cloud Shell**: https://console.cloud.google.com/?cloudshell=true
2. ✅ **Run the command block** (copy entire block above)
3. ✅ **Wait 1-2 minutes** for permissions to propagate
4. ✅ **Re-run GitHub Actions workflow**: https://github.com/BrooCode/happy-scroll-ai/actions
5. ✅ **Watch it succeed!** 🎉

---

**After running the commands, let me know and I'll help you re-run the deployment!**
