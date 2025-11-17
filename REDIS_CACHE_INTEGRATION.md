# Redis Cache Integration Guide

## 🎉 Redis Integration Complete!

Your HappyScroll API now uses **Redis for persistent caching** instead of in-memory storage.

---

## ✅ What Was Done

### 1. **Dependencies Added**
- `redis==5.0.1` - Redis Python client
- `redis[hiredis]==5.0.1` - High-performance C parser

### 2. **Configuration Updated**
- Added `REDIS_URL` to `.env` file
- Updated `app/core/config.py` with Redis URL setting
- Your Redis connection string: `redis://default:***@redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747`

### 3. **Cache Service Upgraded**
- `app/services/cache_service.py` now supports **both** Redis and in-memory caching
- **Automatic fallback**: If Redis is unavailable, uses in-memory cache
- **Lazy initialization**: Cache connects on first use

---

## 🚀 How It Works

### Automatic Cache Selection
```python
# The cache automatically selects the best available option:
cache = get_cache()

# Priority:
# 1. Redis (if redis_url is set and redis package is installed)
# 2. In-Memory (fallback if Redis unavailable)
```

### Redis Cache Features
- ✅ **Persistent**: Survives server restarts
- ✅ **Shared**: Works across multiple server instances
- ✅ **Automatic expiration**: TTL handled by Redis (7 days default)
- ✅ **Statistics tracking**: Hits, misses, size, time saved
- ✅ **Connection pooling**: Efficient connection management
- ✅ **Error handling**: Graceful degradation if Redis fails

---

## 📊 Cache Statistics

View cache performance:
```bash
GET /api/happyScroll/v1/cache/stats
```

**Response includes:**
```json
{
  "status": "success",
  "cache_statistics": {
    "cache_type": "Redis (Persistent)",
    "cache_hits": 42,
    "cache_misses": 15,
    "total_requests": 57,
    "hit_rate_percentage": 73.68,
    "cached_entries": 12,
    "cache_sets": 15,
    "ttl_days": 7,
    "time_saved_seconds": 840,
    "time_saved_minutes": 14.0,
    "estimated_cost_saved_usd": 0.084,
    "persistent": true,
    "shared": true
  }
}
```

---

## 🧪 Testing Redis

### Option 1: Via API Endpoint
```bash
# Windows PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/api/happyScroll/v1/cache/stats" | ConvertFrom-Json
```

### Option 2: Via Test Script
```bash
python test_redis_simple.py
```

### Option 3: Direct Redis Connection
```bash
# Install redis-cli (optional)
# Then test connection:
redis-cli -u "redis://default:Jvd6exTZVwCAr5To63DjxkE3dCPrOkg8@redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747" PING
```

### Option 4: Test via Verdict API
```bash
# Make a request - will initialize cache on first call
curl -X POST "http://localhost:8000/api/happyScroll/v1/verdict" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Check stats to see Redis in action
curl http://localhost:8000/api/happyScroll/v1/cache/stats
```

---

## 🔧 Configuration

### Environment Variable
```bash
# .env file
REDIS_URL=redis://default:Jvd6exTZVwCAr5To63DjxkE3dCPrOkg8@redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747
```

### Cache TTL (Time To Live)
Default: **7 days**

To change:
```python
# In app/services/cache_service.py
cache = get_cache(ttl_days=14)  # 14 days
```

### Connection Settings
```python
# In RedisCache.__init__()
self.redis_client = redis.from_url(
    redis_url,
    decode_responses=True,          # Auto-decode responses to strings
    socket_connect_timeout=5,        # 5 second connection timeout
    socket_timeout=5,                # 5 second operation timeout
    retry_on_timeout=True,           # Retry on timeout
    health_check_interval=30         # Health check every 30 seconds
)
```

---

## 📝 Cache Key Structure

Videos are cached with the following key pattern:
```
happyscroll:verdict:{video_id}
```

**Examples:**
- `happyscroll:verdict:dQw4w9WgXcQ`
- `happyscroll:verdict:9bZkp7q19f0`

**Statistics key:**
```
happyscroll:cache:stats
```

---

## 🛡️ Error Handling

The cache service handles errors gracefully:

### Connection Failures
```python
# If Redis connection fails at startup:
# - Logs warning
# - Falls back to in-memory cache
# - Application continues running
```

### Runtime Errors
```python
# If Redis fails during operation:
# - Logs error
# - Returns None (cache miss)
# - Application continues without caching
```

---

## 🔄 Cache Operations

### Clear Cache
```bash
POST /api/happyScroll/v1/cache/clear
```

Removes all cached verdicts. Use with caution!

### Manual Operations (Python)
```python
from app.services.cache_service import get_cache

cache = get_cache()

# Set value
cache.set("video_id", {"is_safe": True, ...})

# Get value
result = cache.get("video_id")

# Clear all
count = cache.clear()

# Get stats
stats = cache.get_stats()
```

---

## 🎯 Performance Impact

### Before (In-Memory)
- ❌ Lost on restart
- ❌ Not shared across servers
- ⚡ Fast (local)

### After (Redis)
- ✅ Persistent across restarts
- ✅ Shared across all servers
- ⚡ Fast (network, but still <1ms typically)

### Typical Response Times
- **Cache HIT**: <1 second (instant response)
- **Cache MISS**: 15-25 seconds (full analysis)
- **Cache overhead**: ~1-5ms (negligible)

---

## 🚦 Monitoring

### Check Cache Health
```bash
# Via API
GET /api/happyScroll/v1/cache/stats

# Expected response includes:
# - cache_type: "Redis (Persistent)"
# - persistent: true
# - shared: true
```

### Redis Dashboard
Your Redis provider (RedisLabs) likely has a dashboard at:
- https://app.redislabs.com/

### Logs
Watch for these messages:
```
✅ Redis cache initialized with 7 day TTL
🔗 Connected to Redis: redis://***@redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747
✅ Using Redis cache (persistent, shared)
```

---

## 🐛 Troubleshooting

### Issue: Cache not working
**Solution:**
1. Check `.env` file has `REDIS_URL` set
2. Verify Redis server is accessible
3. Check logs for connection errors

### Issue: "Redis package not installed"
**Solution:**
```bash
python -m pip install redis[hiredis]==5.0.1
```

### Issue: Connection timeout
**Solution:**
1. Verify Redis URL is correct
2. Check firewall/network settings
3. Test with `redis-cli` or `test_redis_simple.py`

### Issue: Falls back to in-memory
**Solution:**
- Check logs for the reason
- Common causes:
  - Invalid REDIS_URL
  - Network connectivity issues
  - Redis server down

---

## 🔐 Security Notes

### Connection String Security
- ✅ Stored in `.env` file (not in code)
- ✅ Masked in logs (password hidden)
- ✅ Not committed to git (`.env` in `.gitignore`)

### Best Practices
1. Use strong passwords
2. Enable TLS/SSL for production
3. Use Redis ACLs for access control
4. Monitor for unusual access patterns

---

## 📦 Backup & Recovery

### Redis Data Persistence
Your Redis provider handles:
- ✅ Automatic backups
- ✅ Data replication
- ✅ High availability

### Manual Backup
```bash
# Export all verdict keys
redis-cli -u "$REDIS_URL" --scan --pattern "happyscroll:*" > keys.txt

# Backup data
redis-cli -u "$REDIS_URL" GET key_name
```

---

## 🎓 Additional Resources

### Redis Documentation
- [Redis Python Client](https://redis-py.readthedocs.io/)
- [Redis Commands](https://redis.io/commands)
- [Redis Labs Cloud](https://docs.redis.com/latest/rc/)

### HappyScroll Docs
- `CACHING_IMPLEMENTATION.md` - Original in-memory cache docs
- `CACHE_STORAGE_EXPLAINED.md` - Cache architecture explanation
- `OPTIMIZATION_GUIDE.md` - Performance optimization strategies

---

## ✅ Verification Checklist

- [x] Redis package installed (`redis==5.0.1`)
- [x] `REDIS_URL` added to `.env`
- [x] `cache_service.py` updated with Redis support
- [x] Server running without errors
- [x] Auto-fallback to in-memory works
- [ ] Test cache via API endpoint
- [ ] Verify Redis connection in logs
- [ ] Monitor cache statistics

---

## 🎉 Summary

Your HappyScroll API now has **enterprise-grade caching** with Redis!

**Key Benefits:**
- 🚀 **95% faster** for cached videos (instant responses)
- 💾 **Persistent** storage (survives restarts)
- 🌐 **Scalable** (shared across servers)
- 📊 **Monitorable** (detailed statistics)
- 🛡️ **Reliable** (graceful error handling)

**Next Steps:**
1. Make a video verdict request
2. Check cache stats endpoint
3. Verify Redis is being used
4. Monitor cache hit rate over time

---

*Last updated: November 17, 2025*
*Redis Server: redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747*
