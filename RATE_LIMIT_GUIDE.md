# 🚨 OpenAI 429 Rate Limit Error - Troubleshooting Guide

## What is a 429 Error?

A **429 "Too Many Requests"** error means you've exceeded OpenAI's rate limits for your account tier.

---

## ✅ Immediate Solutions

### 1. **Wait and Retry** (Quickest Fix)
```
⏱️ Wait 60-120 seconds before trying again
```

The rate limit resets after a short period. Just wait a minute or two.

### 2. **Check Your OpenAI Account**

Visit these links to diagnose:

- **Usage Dashboard**: https://platform.openai.com/account/usage
  - See how many requests you've made
  - Check if you're near your limit

- **Billing Page**: https://platform.openai.com/account/billing
  - Verify payment method is added
  - Check if you have credits/quota remaining

- **API Keys**: https://platform.openai.com/api-keys
  - Verify your key is active
  - Generate a new key if needed

### 3. **Understand Rate Limits by Tier**

| Tier | Usage Required | Moderation Limit |
|------|---------------|------------------|
| **Free** | $0 spent | Very limited (5-10 RPM) |
| **Tier 1** | $5+ spent | 500 RPM |
| **Tier 2** | $50+ spent | 5,000 RPM |
| **Tier 3** | $100+ spent | 10,000 RPM |

RPM = Requests Per Minute

---

## 🔧 What We've Implemented

### Automatic Retry Logic

Your API now includes:

✅ **3 automatic retries** with exponential backoff
✅ **Rate limit detection** with helpful error messages
✅ **Fallback model** support (omni-moderation-latest → text-moderation-latest)
✅ **Smart waiting** between retries (2s, 4s, 8s)

### How It Works:

```
1st Request → Rate Limited (429)
   ↓ Wait 2 seconds
2nd Request → Rate Limited (429)
   ↓ Wait 4 seconds
3rd Request → Rate Limited (429)
   ↓ Wait 8 seconds
4th Request → Success or Final Error
```

---

## 💡 Long-Term Solutions

### Option 1: Add Payment Method (Recommended)

1. Go to: https://platform.openai.com/account/billing
2. Click "Add payment method"
3. Add a credit card
4. Add initial credits ($5-10 minimum)

**Benefits:**
- Higher rate limits immediately
- Pay-as-you-go pricing
- Moderation API is very cheap (~$0.002 per 1K requests)

### Option 2: Implement Client-Side Rate Limiting

In your Chrome extension:

```javascript
// Simple rate limiter
let lastRequestTime = 0;
const MIN_DELAY = 1000; // 1 second between requests

async function moderateContent(text) {
  const now = Date.now();
  const timeSinceLastRequest = now - lastRequestTime;
  
  if (timeSinceLastRequest < MIN_DELAY) {
    await new Promise(r => setTimeout(r, MIN_DELAY - timeSinceLastRequest));
  }
  
  lastRequestTime = Date.now();
  return fetch('/api/moderate', { /* ... */ });
}
```

### Option 3: Implement Caching

Cache results for identical or similar content:

```javascript
const moderationCache = new Map();

function getCacheKey(content) {
  return content.toLowerCase().trim().substring(0, 100);
}

async function moderateWithCache(content) {
  const key = getCacheKey(content);
  
  if (moderationCache.has(key)) {
    return moderationCache.get(key);
  }
  
  const result = await moderateContent(content);
  moderationCache.set(key, result);
  
  return result;
}
```

---

## 🧪 Test Your Current Status

Run this PowerShell command to test:

```powershell
$body = @{ content = "Test message" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/moderate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Expected Behaviors:

✅ **Success** - You'll see moderation results
```json
{
  "allowed": true,
  "safe": true,
  "categories": {...}
}
```

⚠️ **Rate Limited** - You'll see a helpful error:
```json
{
  "detail": "Rate limit exceeded. Please wait a moment and try again..."
}
```

❌ **Auth Error** - Check your API key
```json
{
  "detail": "Authentication failed..."
}
```

---

## 📊 Monitoring Rate Limits

Check server logs for retry attempts:

```
2025-11-09 23:03:14 | WARNING | Rate limit hit (attempt 1/3). Waiting 2 seconds...
2025-11-09 23:03:16 | WARNING | Rate limit hit (attempt 2/3). Waiting 4 seconds...
2025-11-09 23:03:20 | INFO    | Moderation complete - Safe: True
```

---

## 🎯 Recommended Next Steps

1. ✅ **Wait 2 minutes** before testing again
2. ✅ **Check your OpenAI dashboard** for usage/billing
3. ✅ **Add payment method** to OpenAI account (if free tier)
4. ✅ **Implement rate limiting** in your Chrome extension
5. ✅ **Consider caching** frequently moderated content

---

## 💰 Cost Estimate

OpenAI Moderation API is very affordable:

- **Price**: ~$0.002 per 1,000 requests
- **Example**: 10,000 moderations = $0.02 (2 cents)
- **100,000 moderations/month** = $0.20 (20 cents)

Adding payment unlocks higher limits for pennies!

---

## 🆘 Still Having Issues?

1. **Check OpenAI Status**: https://status.openai.com/
2. **Review API Docs**: https://platform.openai.com/docs/guides/moderation
3. **Contact OpenAI Support**: https://help.openai.com/

---

**Server automatically retries 3 times with exponential backoff.**
**If all retries fail, the error message will guide you to the solution.**
