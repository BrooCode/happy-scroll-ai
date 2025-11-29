# Branch Protection Setup Guide

## 🔒 Protecting the Main Branch

To ensure only you (BrooCode) can push to `main`, follow these steps:

### Step 1: Go to Repository Settings

1. Navigate to: https://github.com/BrooCode/happy-scroll-ai/settings
2. Click **"Branches"** in the left sidebar

### Step 2: Add Branch Protection Rule

1. Click **"Add branch protection rule"** or **"Add rule"**
2. Enter branch name pattern: `main`

### Step 3: Configure These Settings

#### ✅ **Required Settings**

```
☑ Require a pull request before merging
  ☑ Require approvals: 1
  ☑ Dismiss stale pull request approvals when new commits are pushed
  ☑ Require review from Code Owners

☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  ☑ Status checks that are required:
      - build (GitHub Actions)

☑ Require conversation resolution before merging

☑ Require signed commits (optional but recommended)

☑ Restrict who can push to matching branches
  👤 Add: BrooCode (only you)

☑ Do not allow bypassing the above settings

☐ Allow force pushes (KEEP UNCHECKED)
☐ Allow deletions (KEEP UNCHECKED)
```

### Step 4: Save Changes

Click **"Create"** or **"Save changes"** at the bottom.

---

## 🎯 What This Achieves

### Direct Push Access
- ✅ **You (BrooCode)**: Can push directly to `main`
- ❌ **Everyone else**: Cannot push to `main`

### Pull Requests
- ✅ **Anyone**: Can fork and create PRs
- ❌ **Others**: Cannot merge their own PRs
- ✅ **You**: Sole authority to review and merge PRs

### Repository Visibility
- ✅ **Public**: Anyone can view, clone, and fork
- ✅ **Protected**: Only you can modify `main` branch

---

## 🚀 Using GitHub CLI (Alternative Method)

If you prefer command line:

```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Authenticate
gh auth login

# Enable branch protection (run from repo directory)
gh api repos/BrooCode/happy-scroll-ai/branches/main/protection `
  -X PUT `
  -H "Accept: application/vnd.github+json" `
  -f required_pull_request_reviews='{"required_approving_review_count":1,"require_code_owner_reviews":true,"dismiss_stale_reviews":true}' `
  -f restrictions='{"users":["BrooCode"],"teams":[],"apps":[]}' `
  -f enforce_admins=true `
  -f required_status_checks='{"strict":true,"contexts":["build"]}' `
  -f allow_force_pushes=false `
  -f allow_deletions=false
```

---

## 📊 Verification

After setup, verify protection is active:

```powershell
# Check branch protection status
gh api repos/BrooCode/happy-scroll-ai/branches/main/protection

# Or view on GitHub
# https://github.com/BrooCode/happy-scroll-ai/settings/branches
```

---

## 🔐 Additional Security

### Make Repository Private (If Needed Later)

1. Go to Settings → General
2. Scroll to "Danger Zone"
3. Click "Change repository visibility"
4. Select "Make private"

### Enable Dependency Alerts

1. Settings → Security & analysis
2. Enable "Dependency graph"
3. Enable "Dependabot alerts"
4. Enable "Dependabot security updates"

---

## ✅ Confirmation Checklist

After setup, confirm:

- [ ] Branch protection rule shows "main" is protected
- [ ] "Restrict who can push" lists only your username
- [ ] "Require pull request reviews" is enabled
- [ ] Force pushes and deletions are disabled
- [ ] CODEOWNERS file is in `.github/CODEOWNERS`
- [ ] CONTRIBUTING.md exists in repository root

---

**Setup Complete!** 🎉

Your repository is now public but secure. Only you can push to `main`.
