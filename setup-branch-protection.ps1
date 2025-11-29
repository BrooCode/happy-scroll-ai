# Branch Protection Setup Script for GitHub
# Run this after pushing the CODEOWNERS and workflow files

Write-Host "🔒 Setting up Branch Protection for happy-scroll-ai" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghInstalled) {
    Write-Host "❌ GitHub CLI (gh) not found!" -ForegroundColor Red
    Write-Host "📦 Installing GitHub CLI..." -ForegroundColor Yellow
    winget install --id GitHub.cli
    Write-Host "✅ GitHub CLI installed. Please run this script again." -ForegroundColor Green
    exit
}

Write-Host "✅ GitHub CLI found" -ForegroundColor Green
Write-Host ""

# Check authentication
Write-Host "🔑 Checking GitHub authentication..." -ForegroundColor Cyan
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not authenticated with GitHub" -ForegroundColor Red
    Write-Host "🔐 Logging in to GitHub..." -ForegroundColor Yellow
    gh auth login
} else {
    Write-Host "✅ Already authenticated" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Current repository: BrooCode/happy-scroll-ai" -ForegroundColor Cyan
Write-Host ""

# Confirm action
Write-Host "⚠️  This will:" -ForegroundColor Yellow
Write-Host "   1. Protect the 'main' branch" -ForegroundColor White
Write-Host "   2. Restrict pushes to @BrooCode only" -ForegroundColor White
Write-Host "   3. Require PR reviews before merging" -ForegroundColor White
Write-Host "   4. Enable automated PR checks" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Setup cancelled" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "🔧 Applying branch protection rules..." -ForegroundColor Cyan

# Enable branch protection using GitHub API
$protectionConfig = @{
    required_status_checks = @{
        strict = $true
        contexts = @("all-checks-passed")
    }
    enforce_admins = $true
    required_pull_request_reviews = @{
        required_approving_review_count = 1
        require_code_owner_reviews = $true
        dismiss_stale_reviews = $true
    }
    restrictions = @{
        users = @("BrooCode")
        teams = @()
        apps = @()
    }
    allow_force_pushes = $false
    allow_deletions = $false
    required_conversation_resolution = $true
}

# Convert to JSON
$json = $protectionConfig | ConvertTo-Json -Depth 10

# Apply protection
try {
    gh api repos/BrooCode/happy-scroll-ai/branches/main/protection `
        -X PUT `
        -H "Accept: application/vnd.github+json" `
        --input - <<< $json
    
    Write-Host ""
    Write-Host "✅ Branch protection enabled successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Protection Summary:" -ForegroundColor Cyan
    Write-Host "   ✅ Main branch is now protected" -ForegroundColor Green
    Write-Host "   ✅ Only @BrooCode can push to main" -ForegroundColor Green
    Write-Host "   ✅ PRs require 1 approval" -ForegroundColor Green
    Write-Host "   ✅ Force pushes disabled" -ForegroundColor Green
    Write-Host "   ✅ Branch deletion disabled" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Verify at: https://github.com/BrooCode/happy-scroll-ai/settings/branches" -ForegroundColor Cyan
    
} catch {
    Write-Host ""
    Write-Host "❌ Error applying branch protection!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "📖 Manual setup instructions: .github/BRANCH_PROTECTION_SETUP.md" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • CONTRIBUTING.md - How others can contribute" -ForegroundColor White
Write-Host "   • REPOSITORY_ACCESS.md - Access levels explained" -ForegroundColor White
Write-Host "   • .github/CODEOWNERS - Code ownership rules" -ForegroundColor White
Write-Host "   • .github/workflows/pr-checks.yml - Automated PR checks" -ForegroundColor White
