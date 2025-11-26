# Fix Secret Manager Permissions for Cloud Run

## 🔴 The Problem

Cloud Run is trying to access secrets using the **default Compute Engine service account**:
- Account: `561892525706-compute@developer.gserviceaccount.com`
- This account doesn't have permission to read secrets

## 🔧 Solution: Grant Secret Manager Access

### **Open Google Cloud Shell**
👉 **https://console.cloud.google.com/?cloudshell=true**

### **Run This Command Block**

```bash
# Set project
gcloud config set project happyscroll-478318

echo "🔐 Granting Secret Manager access to Compute Engine service account..."

# Get the project number
PROJECT_NUMBER=$(gcloud projects describe happyscroll-478318 --format="value(projectNumber)")
echo "Project Number: $PROJECT_NUMBER"

# Grant Secret Manager Secret Accessor to Compute Engine service account
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --quiet

# Also grant to your custom service account (if you want to use it)
gcloud projects add-iam-policy-binding happyscroll-478318 \
  --member="serviceAccount:happy-scroll@happyscroll-478318.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --quiet

echo ""
echo "✅ Secret Manager permissions granted!"
echo ""
echo "🔍 Verifying secrets exist..."
gcloud secrets list --project=happyscroll-478318

echo ""
echo "📝 Granting access to individual secrets..."

# Grant access to each secret
gcloud secrets add-iam-policy-binding YOUTUBE_API_KEY \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=happyscroll-478318

gcloud secrets add-iam-policy-binding GOOGLE_VISION_KEY \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=happyscroll-478318

gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=happyscroll-478318

echo ""
echo "🎉 Setup complete! Re-run your GitHub Actions workflow now."
```

---

## ✅ What This Does

1. **Grants Secret Manager Secret Accessor** to the Compute Engine service account
2. **Verifies secrets exist** in Secret Manager
3. Allows Cloud Run to read: `youtube_api_key`, `google_vision_key`, `gemini_key`

---

## 🐛 If Secrets Don't Exist

If the `gcloud secrets list` shows no secrets, create them:

```bash
# Create secrets (replace with your actual values)
echo -n "your-youtube-api-key" | gcloud secrets create youtube_api_key \
  --data-file=- \
  --replication-policy="automatic" \
  --project=happyscroll-478318

echo -n "your-google-vision-key" | gcloud secrets create google_vision_key \
  --data-file=- \
  --replication-policy="automatic" \
  --project=happyscroll-478318

echo -n "your-gemini-api-key" | gcloud secrets create gemini_key \
  --data-file=- \
  --replication-policy="automatic" \
  --project=happyscroll-478318

echo "✅ Secrets created!"
```

---

## 🎯 After Running the Command

1. ✅ **Wait 1 minute** for permissions to propagate
2. ✅ **Go to GitHub Actions**: https://github.com/BrooCode/happy-scroll-ai/actions
3. ✅ **Click the failed workflow**
4. ✅ **Click "Re-run all jobs"** (top right)
5. ✅ **Watch it deploy successfully!** 🚀

---

## 📋 Summary of Required Permissions

### For Deployment (happy-scroll@ service account):
- ✅ Artifact Registry Writer
- ✅ Cloud Run Admin
- ✅ Service Account User
- ✅ Secret Manager Secret Accessor

### For Runtime (Compute Engine service account):
- ✅ **Secret Manager Secret Accessor** ← THIS IS WHAT'S MISSING!

---

**Run the command in Cloud Shell, then re-run your GitHub Actions workflow!** 🎉
