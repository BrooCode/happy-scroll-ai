# 🛡️ Rate Limiting System - Updated

## Overview

The Happy Scroll AI API uses a **two-layer rate limiting system** to manage costs while providing the best user experience:

1. **Client-Side (Chrome Extension)**: 8 videos per user per day
2. **Server-Side (API)**: 150 NEW video analyses per day across all users

---

## 🎯 Key Features

### **Smart Rate Limiting**
- ✅ **Cached videos don't count** toward the API limit
- ✅ Only NEW video analyses are counted
- ✅ Encourages cache hits for better performance
- ✅ Users can check unlimited cached videos

### **Why This Matters**
Popular videos are often checked multiple times. With our caching system:
- **First request**: Counts toward limit (full analysis ~20 seconds)
- **Subsequent requests**: FREE and instant (<1 second)
- **Cache duration**: 7 days

---

## 📊 Rate Limit Configuration

### **API Backend**

```python
GLOBAL_DAILY_LIMIT = 150  # NEW video analyses per day
```

**Behavior:**
- Cache HIT: ✅ **Does NOT count** toward limit
- Cache MISS: ❌ **Counts** toward limit (triggers new analysis)

**Example Scenario:**
- User 1 checks video A (NEW) → Counter: 1/150 ✅
- User 2 checks video A (CACHED) → Counter: 1/150 ✅ (no change)
- User 3 checks video B (NEW) → Counter: 2/150 ✅
- User 4 checks video A (CACHED) → Counter: 2/150 ✅ (no change)

### **Chrome Extension**

```javascript
MAX_VIDEOS_PER_DAY = 8  // Videos per user per day
```

**Behavior:**
- Each user can check 8 videos per day
- Resets at midnight local time
- Applies regardless of cache status

---

## 🔄 How It Works

### **Request Flow**

```
1. User requests video analysis
2. API checks: Is limit reached? (150 NEW analyses)
   ├─ YES → Return 429 error
   └─ NO → Continue
3. Check cache: Is video cached?
   ├─ YES → Return cached result (instant, FREE) ⚡
   └─ NO → Perform new analysis:
       ├─ Increment counter (now counts as 1 NEW analysis)
       ├─ Analyze transcript (Gemini AI)
       ├─ Analyze thumbnail (Google Vision)
       ├─ Cache result (7 days)
       └─ Return result
```

### **Code Implementation**

```python
# Check limit WITHOUT incrementing
limit_info = check_global_limit(increment=False)

# Check cache first
cached_result = cache.get(video_id)
if cached_result:
    # Cache HIT - return immediately (no counter increment)
    return cached_result

# Cache MISS - increment counter for NEW analysis
limit_info = check_global_limit(increment=True)

# Perform analysis...
```

---

## 📈 Cost Impact

### **Old System (100 requests/day, all counted)**
- All requests counted toward limit
- Cache hits wasted quota
- 100 analyses per day

### **New System (150 NEW analyses/day, cache excluded)**
- Only new analyses count
- Cache hits are FREE
- With 70% cache hit rate:
  - 150 new analyses
  - ~350 cached responses (free)
  - **Total: ~500 video checks per day**

### **Cost Estimate**

**Per NEW Video Analysis:**
- Gemini API: ~$0.002
- Google Vision API: ~$0.003
- Cloud Run: ~$0.0001
- **Total: ~$0.005 per analysis**

**Daily Costs:**
- 150 new analyses × $0.005 = **$0.75/day**
- **Monthly: ~$22.50**

**With Cache Benefits:**
- Actual user requests: 500 checks/day
- Cost: Still only $0.75/day (cache is free)
- **Effective cost per check: $0.0015** (70% savings)

---

## 🎮 User Experience

### **Extension User (8 videos/day limit)**

```
User checks 8 videos:
├─ Video 1 (NEW) → 2 seconds (analysis)
├─ Video 2 (NEW) → 2 seconds (analysis)
├─ Video 3 (CACHED) → <1 second ⚡
├─ Video 4 (NEW) → 2 seconds (analysis)
├─ Video 5 (CACHED) → <1 second ⚡
├─ Video 6 (NEW) → 2 seconds (analysis)
├─ Video 7 (CACHED) → <1 second ⚡
└─ Video 8 (NEW) → 2 seconds (analysis)

User's experience:
- 5 new analyses (counted toward API limit)
- 3 instant cached results (FREE)
- Limit reached: "8 videos checked today"
```

### **API Perspective (150 NEW analyses/day)**

```
Day's activity across ALL users:
├─ 150 NEW video analyses (counted)
├─ 350 cached responses (not counted)
└─ Total: 500 video checks handled

API quota:
- Used: 150/150 NEW analyses
- Cache hits: 350 (free bonus!)
- Effective capacity: 500 checks/day
```

---

## ⚠️ Rate Limit Responses

### **Client-Side (Extension) Limit**

When user reaches 8 videos/day:
```
⚠️ Happy Scroll AI - Daily Limit Reached

You've checked 8 videos today.
Come back tomorrow for more safe browsing! 🚀

This is a demo project with limited free API usage.
```

### **Server-Side (API) Limit**

When API reaches 150 NEW analyses/day:

**HTTP 429 Response:**
```json
{
  "detail": {
    "error": "Daily limit exceeded",
    "message": "Demo API has reached its daily limit for new video analysis.",
    "info": "This is a demo project with limited free tier usage to manage costs.",
    "note": "Cached videos do not count toward the limit.",
    "limit": 150,
    "requests_today": 150
  }
}
```

---

## 🔧 Adjusting Limits

### **API Limit**

Edit `app/routes/happyscroll_verdict.py`:
```python
GLOBAL_DAILY_LIMIT = 150  # Change this number
```

### **Extension Limit**

Edit `Happy Scroll AI/content.js`:
```javascript
const MAX_VIDEOS_PER_DAY = 8;  // Change this number
```

---

## 📊 Monitoring

### **Check Current Status**

```bash
# In Cloud Run logs
grep "Global requests today" /logs
```

### **Cache Statistics**

```bash
curl https://your-api.run.app/api/happyScroll/v1/cache/stats
```

**Response:**
```json
{
  "total_requests": 500,
  "cache_hits": 350,
  "cache_misses": 150,
  "hit_rate": 0.70,
  "cached_entries": 89,
  "efficiency": "High cache efficiency (70% hit rate)"
}
```

---

## 🚀 For Production

To remove limits:

### **Option 1: Increase Limits**
```python
GLOBAL_DAILY_LIMIT = 10000  # Generous limit
```

### **Option 2: Remove Rate Limiting**
```python
# Comment out limit check
# limit_info = check_global_limit(increment=False)
```

### **Option 3: Redis-Based Rate Limiting**
Use Redis for distributed rate limiting across multiple Cloud Run instances:
```python
import redis

redis_client = redis.from_url(settings.redis_url)

def check_limit_with_redis():
    key = f"rate_limit:{datetime.now().date()}"
    count = redis_client.incr(key)
    redis_client.expire(key, 86400)  # 24 hours
    return count <= GLOBAL_DAILY_LIMIT
```

---

## 📝 Summary

| Feature | Value | Notes |
|---------|-------|-------|
| **API Limit** | 150/day | NEW analyses only |
| **Extension Limit** | 8/day | Per user |
| **Cache Duration** | 7 days | Results stored |
| **Cache Benefit** | FREE | Unlimited cached responses |
| **Expected Cache Hit Rate** | 60-80% | Popular videos |
| **Cost per NEW Analysis** | ~$0.005 | With all APIs |
| **Daily Cost** | ~$0.75 | At 150 limit |
| **Monthly Cost** | ~$22.50 | Well within budget |

---

## ✅ Benefits of New System

1. **More Capacity**: 150 NEW + unlimited cached = ~500 total checks/day
2. **Cost Efficient**: Cache hits are free
3. **Better UX**: Instant responses for popular videos
4. **Fair Usage**: Encourages cache utilization
5. **Predictable Costs**: Only pay for new analyses

---

**Last Updated**: November 29, 2025  
**Version**: 2.0 (Smart Rate Limiting with Cache Exclusion)
