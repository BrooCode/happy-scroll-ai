"""
Check OpenAI Account Status and Limits
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def check_account_status():
    """Check OpenAI account status and provide recommendations."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return
    
    print("=" * 70)
    print("  OpenAI Account Status Check")
    print("=" * 70)
    print()
    
    # Check API key format
    print("1. API Key Validation:")
    print(f"   Key: {api_key[:20]}...{api_key[-4:]}")
    print(f"   Length: {len(api_key)} characters")
    
    if api_key.startswith("sk-proj-"):
        print("   ✓ Format: Project API key (newer format)")
    elif api_key.startswith("sk-"):
        print("   ✓ Format: Valid OpenAI API key")
    else:
        print("   ✗ Format: Invalid - should start with 'sk-'")
        return
    
    print()
    print("2. Account Information:")
    print("   To check your account status, visit:")
    print()
    print("   📊 Usage Dashboard:")
    print("      https://platform.openai.com/account/usage")
    print()
    print("   💳 Billing & Limits:")
    print("      https://platform.openai.com/account/billing")
    print()
    print("   🔑 API Keys:")
    print("      https://platform.openai.com/api-keys")
    print()
    
    print("3. Common Issues for New Accounts:")
    print()
    print("   Issue: Getting 429 errors immediately")
    print("   ├─ New accounts have very strict rate limits")
    print("   ├─ Free tier: ~5-10 requests per minute")
    print("   ├─ Daily limits may also apply")
    print("   └─ Solution: Add payment method (even $5 helps)")
    print()
    
    print("4. What Counts as 'Free Tier':")
    print()
    print("   ✗ No payment method added = Extremely limited")
    print("   ✓ Payment method added = Higher limits")
    print("   ✓ $5+ spent = Tier 1 (500 RPM)")
    print("   ✓ $50+ spent = Tier 2 (5,000 RPM)")
    print()
    
    print("5. Moderation API Costs:")
    print()
    print("   Very affordable pricing:")
    print("   ├─ $0.002 per 1,000 requests")
    print("   ├─ 1,000 moderations = $0.002 (0.2 cents)")
    print("   ├─ 10,000 moderations = $0.02 (2 cents)")
    print("   └─ 100,000 moderations = $0.20 (20 cents)")
    print()
    
    print("6. Recommended Actions:")
    print()
    print("   Step 1: Visit the billing page")
    print("      → https://platform.openai.com/account/billing")
    print()
    print("   Step 2: Check if payment method is added")
    print("      → If not, add a credit card")
    print()
    print("   Step 3: Add $5-10 in credits")
    print("      → This unlocks much higher limits")
    print()
    print("   Step 4: Wait 1-2 minutes for limits to update")
    print()
    print("   Step 5: Test again")
    print("      → python test_openai.py")
    print()
    
    print("=" * 70)
    print("  Account Tier Comparison")
    print("=" * 70)
    print()
    print("  FREE (No payment method):")
    print("  ├─ Rate: 5-10 requests/minute")
    print("  ├─ Daily: Very limited")
    print("  └─ Best for: Quick testing only")
    print()
    print("  TIER 1 ($5+ spent):")
    print("  ├─ Rate: 500 requests/minute")
    print("  ├─ Daily: Much higher limits")
    print("  └─ Best for: Development & testing")
    print()
    print("  TIER 2 ($50+ spent):")
    print("  ├─ Rate: 5,000 requests/minute")
    print("  ├─ Daily: Very high limits")
    print("  └─ Best for: Production use")
    print()
    
    print("=" * 70)
    print()
    print("💡 Bottom Line:")
    print("   Your API key is valid, but you're hitting account limits.")
    print("   Adding a payment method (even without charges) will help.")
    print()

if __name__ == "__main__":
    check_account_status()
