# Cache Storage Location - Explanation

## 🎯 Where Is the Cache Stored?

### **Current Implementation: IN-MEMORY (RAM)**

The cache is stored in **your server's RAM (memory)**, not on disk.

```python
# From app/services/cache_service.py
class VerdictCache:
    def __init__(self, ttl_days: int = 7):
        self.cache: Dict[str, Dict[str, Any]] = {}  # ← Stored in RAM!
```

---

## 📊 Cache Storage Details

### Storage Location
```
┌─────────────────────────────────────────┐
│         Your Server (Computer)          │
├─────────────────────────────────────────┤
│  RAM (Memory)                           │
│  ├─ Python Process                      │
│  │  └─ VerdictCache Object              │
│  │     └─ self.cache = {                │
│  │          "dQw4w9WgXcQ": {...},       │
│  │          "9bZkp7q19f0": {...},       │
│  │        }                              │
└─────────────────────────────────────────┘
```

### What This Means

| Aspect | Details |
|--------|---------|
| **Location** | Server's RAM (not disk) |
| **Persistence** | ❌ Lost on server restart |
| **Shared** | ❌ Not shared between multiple servers |
| **Speed** | ✅ **VERY FAST** (instant access) |
| **Size Limit** | Limited by available RAM |
| **Cost** | ✅ Free (no external service) |

---

## 🔍 Data Structure

### Cache Format

```python
{
    "video_id": {
        "result": {
            "is_safe": True,
            "is_safe_transcript": True,
            "is_safe_thumbnail": True,
            "transcript_reason": "...",
            "thumbnail_reason": "...",
            "overall_reason": "...",
            "video_title": "...",
            "channel_title": "..."
        },
        "cached_at": datetime(2025, 11, 17, 10, 30, 0),
        "expires_at": datetime(2025, 11, 24, 10, 30, 0)  # 7 days later
    }
}
```

### Example

```python
cache = {
    "dQw4w9WgXcQ": {  # Rick Astley video
        "result": {
            "is_safe": True,
            "video_title": "Never Gonna Give You Up",
            # ... other fields
        },
        "cached_at": "2025-11-17 10:30:00",
        "expires_at": "2025-11-24 10:30:00"
    },
    "9bZkp7q19f0": {  # Another video
        "result": {...},
        "cached_at": "2025-11-17 11:00:00",
        "expires_at": "2025-11-24 11:00:00"
    }
}
```

---

## ⚠️ Important Limitations

### 1. **NOT Persistent**

```
Server Restart → Cache Cleared ❌

Before Restart: Cache has 100 videos
After Restart:  Cache is empty (0 videos)
```

**Impact**: First requests after restart will be slow again.

### 2. **NOT Shared Across Servers**

```
Server A: Cache has video X ✅
Server B: Cache is empty ❌

User hits Server A → Fast (cached)
User hits Server B → Slow (not cached)
```

**Impact**: Not ideal for load-balanced deployments.

### 3. **Memory Usage**

```
Each cached video ≈ 1-2 KB
1,000 videos ≈ 1-2 MB
10,000 videos ≈ 10-20 MB
```

**Impact**: Generally not a problem, but can grow if caching millions of videos.

---

## 🔄 Alternative Storage Options

### Option 1: Redis (Recommended for Production)

**Location**: External Redis server (persistent storage)

```python
# Install Redis
pip install redis

# Store in Redis instead of RAM
import redis
redis_client = redis.Redis(host='localhost', port=6379)

def get_cached_verdict(video_id):
    cached = redis_client.get(f"verdict:{video_id}")
    if cached:
        return json.loads(cached)
    return None

def cache_verdict(video_id, result):
    redis_client.setex(
        f"verdict:{video_id}",
        7 * 24 * 3600,  # 7 days
        json.dumps(result)
    )
```

**Benefits**:
- ✅ **Persistent** (survives restarts)
- ✅ **Shared** (multiple servers can use same cache)
- ✅ **Better memory management**
- ✅ **Built-in TTL support**

**Drawbacks**:
- ❌ Requires Redis server
- ❌ Slightly slower than RAM (but still very fast)
- ❌ Additional infrastructure

---

### Option 2: Database (SQLite/PostgreSQL)

**Location**: Database file or database server

```python
# Store in database
def get_cached_verdict(video_id):
    result = db.query(
        "SELECT * FROM cache WHERE video_id = ? AND expires_at > NOW()",
        video_id
    )
    return result

def cache_verdict(video_id, result):
    db.execute(
        "INSERT INTO cache (video_id, result, expires_at) VALUES (?, ?, ?)",
        video_id, result, datetime.now() + timedelta(days=7)
    )
```

**Benefits**:
- ✅ **Persistent** (survives restarts)
- ✅ **Easy to query** and analyze
- ✅ **No additional service** needed (can use existing DB)

**Drawbacks**:
- ❌ Slower than RAM or Redis
- ❌ More complex to manage
- ❌ Not ideal for high-frequency reads

---

### Option 3: File System

**Location**: Files on disk

```python
import json
import os

def get_cached_verdict(video_id):
    cache_file = f"cache/{video_id}.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

def cache_verdict(video_id, result):
    os.makedirs("cache", exist_ok=True)
    with open(f"cache/{video_id}.json", 'w') as f:
        json.dump(result, f)
```

**Benefits**:
- ✅ **Persistent** (survives restarts)
- ✅ **Simple** to implement
- ✅ **No dependencies**

**Drawbacks**:
- ❌ Slow (disk I/O)
- ❌ Poor performance with many files
- ❌ Not suitable for production

---

## 📊 Comparison

| Storage | Speed | Persistent | Shared | Complexity | Cost |
|---------|-------|------------|--------|------------|------|
| **RAM (Current)** | ⚡ Instant | ❌ No | ❌ No | ✅ Simple | Free |
| **Redis** | ⚡ Very Fast | ✅ Yes | ✅ Yes | 🟡 Medium | $-$$ |
| **Database** | 🐌 Slow | ✅ Yes | ✅ Yes | 🟡 Medium | Free-$$ |
| **File System** | 🐢 Very Slow | ✅ Yes | ❌ No | ✅ Simple | Free |

---

## 🎯 Current Cache Storage Summary

### Where Cache Lives

```
Physical Location:
D:\happy-scroll-ai\app\services\cache_service.py
  └─ VerdictCache class
     └─ self.cache = {}  ← Dictionary in RAM

When running:
Your Computer's RAM
  └─ Python Process (uvicorn)
     └─ FastAPI Application
        └─ VerdictCache instance
           └─ cache = {video_id: result}
```

### Lifecycle

```
1. Server Start → Cache is empty {}
2. First Request → Full analysis (20s), cache result
3. Second Request → Return from cache (<1s) ✅
4. After 7 days → Entry expires automatically
5. Server Restart → Cache cleared, back to empty {}
```

---

## 💡 Recommendations

### For Development (Current Setup)
✅ **Use RAM cache** (current implementation)
- Fast and simple
- No setup required
- Perfect for testing

### For Production
✅ **Upgrade to Redis**
- Persistent across restarts
- Shared between servers
- Better for scale

### How to Switch to Redis

1. **Install Redis**:
```bash
# Windows (using Chocolatey)
choco install redis-64

# Or download from: https://redis.io/download
```

2. **Install Python client**:
```bash
pip install redis
```

3. **Update cache service** (I can help you with this!)

---

## 🔧 Viewing Cache Data

### Check What's in Cache

```bash
# Get cache statistics
curl http://localhost:8000/api/happyScroll/v1/cache/stats
```

**Response**:
```json
{
  "cached_entries": 5,  ← 5 videos currently cached
  "cache_hits": 20,
  "cache_misses": 5
}
```

### Cache is Empty If:

- ✅ Server was just started
- ✅ Cache was manually cleared
- ✅ All entries expired (after 7 days)
- ✅ Server crashed/restarted

---

## 🎯 Quick Answer

**Q: Where is cache stored?**

**A:** In your **server's RAM (memory)** as a Python dictionary. It's:
- ⚡ **Very fast** (instant access)
- ❌ **Not persistent** (cleared on restart)
- ❌ **Not shared** (single server only)
- ✅ **Perfect for development**
- 🔄 **Should upgrade to Redis for production**

---

**Want me to help you upgrade to Redis for persistent caching?** 🚀
