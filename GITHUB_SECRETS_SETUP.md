# GitHub Secrets Setup Guide

Before pushing to GitHub, you need to configure the required secrets for automated deployment.

## 📋 Required Secrets

You need to add 3 secrets to your GitHub repository:

### 1. `GCP_PROJECT_ID`
**Value**: `happyscroll-478318`

### 2. `GCP_SA_KEY`
**Value**: Copy the ENTIRE content of `d:\happy-scroll-ai\credentials\happyscroll-478318-6a860e981468.json`

The content should look like:
```json
{
  "type": "service_account",
  "project_id": "happyscroll-478318",
  "private_key_id": "6a860e981468810d116904af293adeb2f2cd958c",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "happy-scroll@happyscroll-478318.iam.gserviceaccount.com",
  ...
}
```

### 3. `REDIS_URL`
**Value**: `redis://default:Jvd6exTZVwCAr5To63DjxkE3dCPrOkg8@redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747`

---

## 🔧 How to Add Secrets to GitHub

### Step 1: Go to Your Repository
Navigate to: **https://github.com/BrooCode/happy-scroll-ai**

### Step 2: Open Settings
Click on **Settings** tab (top right of the repository page)

### Step 3: Navigate to Secrets
1. In the left sidebar, click **Secrets and variables**
2. Click **Actions**

### Step 4: Add Each Secret
For each secret:

1. Click **New repository secret** button
2. Enter the **Name** (exactly as shown above)
3. Paste the **Value**
4. Click **Add secret**

**Repeat for all 3 secrets**.

---

## ✅ Verification

After adding all secrets, you should see:
- ✅ `GCP_PROJECT_ID`
- ✅ `GCP_SA_KEY`
- ✅ `REDIS_URL`

---

## 🚀 Next Steps

Once secrets are configured:

1. **Push to GitHub**:
   ```powershell
   git push origin main
   ```

2. **Monitor Deployment**:
   - Go to **Actions** tab in your GitHub repository
   - Watch the "Deploy to Cloud Run" workflow
   - It will take 5-10 minutes to complete

3. **Get Your Deployment URL**:
   - After successful deployment, check the workflow logs
   - Your API will be at: `https://happy-scroll-service-XXXXX-uc.a.run.app`

---

## 📝 Notes

- **Security**: Never commit these secrets to your repository
- **Service Account Key**: The JSON file is already in `.gitignore`
- **Secrets Access**: Only GitHub Actions workflows can access these secrets
- **Updates**: If you need to change a secret, go to Settings → Secrets → Actions and update it

---

## 🐛 Troubleshooting

**If deployment fails**:

1. Check the Actions tab for error messages
2. Verify all 3 secrets are added correctly
3. Ensure the service account has the required permissions
4. Check that Cloud Run API and Artifact Registry API are enabled in GCP

**Common Issues**:

- **"Permission denied"**: Service account missing roles
- **"Secret not found"**: Secrets not added to GitHub or wrong names
- **"Repository not found"**: Artifact Registry repository not created

---

## 📞 Support

If you encounter issues, check the GitHub Actions logs for detailed error messages.
