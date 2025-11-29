# 🔒 Repository Access & Security

## Public Repository with Protected Main Branch

This repository is **publicly accessible** for viewing, cloning, and forking, but the `main` branch is **protected** and can only be modified by the maintainer (@BrooCode).

---

## 🎯 Access Levels

### Everyone (Public Access)
✅ View all code and documentation  
✅ Clone the repository  
✅ Fork the repository  
✅ Create issues  
✅ Submit pull requests  
❌ Push directly to `main` branch  
❌ Merge pull requests  

### Maintainer Only (@BrooCode)
✅ All public access permissions  
✅ Push directly to `main` branch  
✅ Merge pull requests  
✅ Modify repository settings  
✅ Manage releases and deployments  

---

## 🛡️ Branch Protection Rules

The `main` branch has the following protections:

### 🔐 Push Restrictions
- **Only @BrooCode can push** directly to `main`
- All other users must submit pull requests

### ✅ Pull Request Requirements
- Requires **1 approval** from code owner (@BrooCode)
- Must pass all **CI/CD checks**:
  - Code linting (Black, Flake8)
  - Unit tests
  - Security scanning
  - Secret detection
- Conversations must be resolved
- Branch must be up to date

### 🚫 Disabled Actions
- ❌ Force pushes (prevents history rewriting)
- ❌ Branch deletion (protects main branch)
- ❌ Bypass protection rules (no exceptions)

---

## 📝 How to Contribute

Since you cannot push directly to `main`, follow this workflow:

### Step 1: Fork the Repository
```bash
# Click "Fork" button on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/happy-scroll-ai.git
cd happy-scroll-ai
```

### Step 2: Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Step 3: Make Changes
```bash
# Make your changes
git add .
git commit -m "Add: your feature description"
```

### Step 4: Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### Step 5: Create Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch → original repo's main branch
4. Fill in PR description
5. Submit for review

### Step 6: Wait for Review
- @BrooCode will review your PR
- Address any feedback
- Once approved, @BrooCode will merge

---

## 🤖 Automated Checks

All pull requests automatically run these checks:

| Check | Purpose | Status Required |
|-------|---------|-----------------|
| **Source Verification** | Ensures PR is from feature branch | ✅ Required |
| **Code Linting** | Black formatter + Flake8 | ⚠️ Warning only |
| **Unit Tests** | Pytest with coverage | ⚠️ Warning only |
| **Security Scan** | Trivy vulnerability scanner | ✅ Required |
| **Secret Detection** | Scans for exposed keys/passwords | ✅ Required |
| **PR Size Check** | Warns if PR is too large (>1000 lines) | ⚠️ Warning only |

---

## 🔍 Code Ownership

All code changes require approval from designated code owners (defined in `.github/CODEOWNERS`):

```
# All files require @BrooCode approval
* @BrooCode

# Critical paths
/.github/* @BrooCode
/app/* @BrooCode
/Dockerfile @BrooCode
```

---

## 🚨 Security Measures

### Protected Information
- ✅ API keys stored in Google Cloud Secret Manager
- ✅ No secrets committed to repository
- ✅ `.gitignore` excludes sensitive files
- ✅ Automated secret scanning on all PRs

### Dependency Security
- ✅ Dependabot alerts enabled
- ✅ Regular security updates
- ✅ Vulnerability scanning in CI/CD

### Access Control
- ✅ Branch protection rules enforced
- ✅ Required reviews for all changes
- ✅ No force push allowed
- ✅ Signed commits recommended

---

## 📋 For Repository Maintainer

### Setting Up Branch Protection

1. **Via GitHub UI:**
   - Go to: Settings → Branches
   - Add rule for `main` branch
   - Configure restrictions
   - See: `.github/BRANCH_PROTECTION_SETUP.md`

2. **Via GitHub CLI:**
   ```powershell
   gh api repos/BrooCode/happy-scroll-ai/branches/main/protection \
     -X PUT \
     -H "Accept: application/vnd.github+json" \
     -f restrictions='{"users":["BrooCode"],"teams":[],"apps":[]}'
   ```

### Managing Pull Requests

```bash
# List open PRs
gh pr list

# Review a PR
gh pr review <PR_NUMBER> --approve -b "LGTM!"

# Merge approved PR
gh pr merge <PR_NUMBER> --squash

# Close PR without merging
gh pr close <PR_NUMBER>
```

---

## 🎓 Best Practices for Contributors

### Do's ✅
- Create descriptive branch names (`feature/add-caching`)
- Write clear commit messages
- Keep PRs focused and small
- Add tests for new features
- Update documentation
- Respond to review feedback promptly

### Don'ts ❌
- Don't try to push directly to `main`
- Don't include unrelated changes
- Don't commit sensitive information
- Don't force push to shared branches
- Don't ignore CI/CD failures

---

## 🔗 Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [.github/CODEOWNERS](.github/CODEOWNERS) - Code ownership rules
- [.github/BRANCH_PROTECTION_SETUP.md](.github/BRANCH_PROTECTION_SETUP.md) - Setup guide

---

## 📞 Questions?

If you have questions about access or contributions:
- Open an [issue](https://github.com/BrooCode/happy-scroll-ai/issues)
- Start a [discussion](https://github.com/BrooCode/happy-scroll-ai/discussions)
- Tag @BrooCode in your PR

---

**Repository Status: Public | Main Branch: Protected | Maintainer: @BrooCode**
