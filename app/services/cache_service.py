"""
Cache Service for HappyScroll Verdict API
Provides both Redis and in-memory caching to speed up repeated video analysis requests
"""
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from loguru import logger

try:
    import redis
    from redis.exceptions import ConnectionError, TimeoutError, RedisError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("⚠️  Redis package not installed. Using in-memory cache only.")


class BaseCache:
    """Base cache interface"""
    
    def get(self, video_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
    
    def set(self, video_id: str, result: Dict[str, Any]) -> None:
        raise NotImplementedError
    
    def clear(self) -> int:
        raise NotImplementedError
    
    def get_stats(self) -> Dict[str, Any]:
        raise NotImplementedError


class RedisCache(BaseCache):
    """
    Redis-based cache for video verdict results
    
    Features:
    - Persistent storage across server restarts
    - Shared across multiple server instances
    - TTL (Time To Live) based expiration
    - Automatic cleanup by Redis
    - Connection pooling
    """
    
    def __init__(self, redis_url: str, ttl_days: int = 7):
        """
        Initialize Redis cache
        
        Args:
            redis_url: Redis connection URL
            ttl_days: Number of days to cache results (default: 7)
        """
        self.ttl_seconds = int(timedelta(days=ttl_days).total_seconds())
        self.ttl_days = ttl_days
        
        try:
            # Create Redis connection with connection pooling
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info(f"✅ Redis cache initialized with {ttl_days} day TTL")
            logger.info(f"🔗 Connected to Redis: {self._mask_url(redis_url)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {str(e)}")
            raise ConnectionError(f"Redis connection failed: {str(e)}")
    
    def _mask_url(self, url: str) -> str:
        """Mask sensitive parts of Redis URL for logging"""
        if "@" in url:
            parts = url.split("@")
            return f"redis://***@{parts[1]}"
        return url
    
    def _get_key(self, video_id: str) -> str:
        """Generate Redis key for video"""
        return f"happyscroll:verdict:{video_id}"
    
    def _get_stats_key(self) -> str:
        """Get key for cache statistics"""
        return "happyscroll:cache:stats"
    
    def get(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cached result for video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Cached verdict result or None if not found/expired
        """
        try:
            key = self._get_key(video_id)
            cached_data = self.redis_client.get(key)
            
            if cached_data is None:
                # Cache miss - increment miss counter
                self.redis_client.hincrby(self._get_stats_key(), "misses", 1)
                logger.debug(f"Cache MISS: {video_id}")
                return None
            
            # Cache hit - increment hit counter
            self.redis_client.hincrby(self._get_stats_key(), "hits", 1)
            logger.info(f"✅ Redis Cache HIT: {video_id} (saved ~20s)")
            
            # Parse JSON data
            result = json.loads(cached_data)
            return result
            
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"❌ Redis connection error on GET: {str(e)}")
            self.redis_client.hincrby(self._get_stats_key(), "misses", 1)
            return None
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to decode cached data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"❌ Redis GET error: {str(e)}")
            return None
    
    def set(self, video_id: str, result: Dict[str, Any]) -> None:
        """
        Cache verdict result for video
        
        Args:
            video_id: YouTube video ID
            result: Verdict result to cache
        """
        try:
            key = self._get_key(video_id)
            
            # Serialize result to JSON
            cached_data = json.dumps(result)
            
            # Set with TTL
            self.redis_client.setex(key, self.ttl_seconds, cached_data)
            
            # Increment set counter
            self.redis_client.hincrby(self._get_stats_key(), "sets", 1)
            
            logger.info(f"💾 Redis: Cached result for {video_id} (expires in {self.ttl_days} days)")
            
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"❌ Redis connection error on SET: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Redis SET error: {str(e)}")
    
    def clear(self) -> int:
        """
        Clear all cached verdict entries
        
        Returns:
            Number of entries cleared
        """
        try:
            # Find all verdict keys
            pattern = "happyscroll:verdict:*"
            keys = list(self.redis_client.scan_iter(match=pattern))
            
            if keys:
                count = self.redis_client.delete(*keys)
                logger.info(f"🗑️  Redis: Cache cleared - {count} entries removed")
                return count
            else:
                logger.info("🗑️  Redis: No cache entries to clear")
                return 0
                
        except Exception as e:
            logger.error(f"❌ Redis CLEAR error: {str(e)}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            stats_key = self._get_stats_key()
            
            # Get statistics from Redis hash
            stats_data = self.redis_client.hgetall(stats_key)
            
            hits = int(stats_data.get("hits", 0))
            misses = int(stats_data.get("misses", 0))
            sets = int(stats_data.get("sets", 0))
            
            # Count current cached entries
            pattern = "happyscroll:verdict:*"
            cached_entries = sum(1 for _ in self.redis_client.scan_iter(match=pattern, count=100))
            
            total_requests = hits + misses
            hit_rate = (hits / total_requests * 100) if total_requests > 0 else 0
            
            # Calculate time saved (assuming 20s per cache hit)
            time_saved_seconds = hits * 20
            time_saved_minutes = time_saved_seconds / 60
            
            return {
                "cache_type": "Redis (Persistent)",
                "cache_hits": hits,
                "cache_misses": misses,
                "total_requests": total_requests,
                "hit_rate_percentage": round(hit_rate, 2),
                "cached_entries": cached_entries,
                "cache_sets": sets,
                "ttl_days": self.ttl_days,
                "time_saved_seconds": time_saved_seconds,
                "time_saved_minutes": round(time_saved_minutes, 2),
                "estimated_cost_saved_usd": round(hits * 0.002, 4),
                "persistent": True,
                "shared": True
            }
            
        except Exception as e:
            logger.error(f"❌ Redis STATS error: {str(e)}")
            return {
                "cache_type": "Redis (Error)",
                "error": str(e),
                "cache_hits": 0,
                "cache_misses": 0,
                "total_requests": 0,
                "hit_rate_percentage": 0.0,
                "cached_entries": 0
            }


class InMemoryCache(BaseCache):
    """
    In-memory cache for video verdict results (fallback)
    
    Features:
    - Fast local caching
    - TTL based expiration
    - No external dependencies
    - Lost on server restart
    """
    
    def __init__(self, ttl_days: int = 7):
        """
        Initialize in-memory cache
        
        Args:
            ttl_days: Number of days to cache results (default: 7)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = timedelta(days=ttl_days)
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "size": 0
        }
        logger.info(f"✅ In-memory cache initialized with {ttl_days} day TTL")
        logger.warning("⚠️  Using in-memory cache - data will be lost on restart")
    
    def get(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get cached result for video"""
        if video_id not in self.cache:
            self.stats["misses"] += 1
            logger.debug(f"Cache MISS: {video_id}")
            return None
        
        entry = self.cache[video_id]
        
        # Check if expired
        if datetime.now() > entry["expires_at"]:
            logger.debug(f"Cache EXPIRED: {video_id}")
            del self.cache[video_id]
            self.stats["misses"] += 1
            self.stats["size"] = len(self.cache)
            return None
        
        # Cache hit
        self.stats["hits"] += 1
        logger.info(f"✅ Memory Cache HIT: {video_id} (saved ~20s)")
        return entry["result"]
    
    def set(self, video_id: str, result: Dict[str, Any]) -> None:
        """Cache verdict result for video"""
        self.cache[video_id] = {
            "result": result,
            "cached_at": datetime.now(),
            "expires_at": datetime.now() + self.ttl
        }
        self.stats["sets"] += 1
        self.stats["size"] = len(self.cache)
        logger.info(f"💾 Memory: Cached result for {video_id} (expires in {self.ttl.days} days)")
    
    def clear(self) -> int:
        """Clear all cached entries"""
        count = len(self.cache)
        self.cache.clear()
        self.stats["size"] = 0
        logger.info(f"🗑️  Memory: Cache cleared - {count} entries removed")
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        time_saved_seconds = self.stats["hits"] * 20
        time_saved_minutes = time_saved_seconds / 60
        
        return {
            "cache_type": "In-Memory (Non-Persistent)",
            "cache_hits": self.stats["hits"],
            "cache_misses": self.stats["misses"],
            "total_requests": total_requests,
            "hit_rate_percentage": round(hit_rate, 2),
            "cached_entries": self.stats["size"],
            "cache_sets": self.stats["sets"],
            "ttl_days": self.ttl.days,
            "time_saved_seconds": time_saved_seconds,
            "time_saved_minutes": round(time_saved_minutes, 2),
            "estimated_cost_saved_usd": round(self.stats["hits"] * 0.002, 4),
            "persistent": False,
            "shared": False
        }


# Global cache instance
_cache_instance: Optional[BaseCache] = None


def get_cache(ttl_days: int = 7, redis_url: Optional[str] = None) -> BaseCache:
    """
    Get or create the global cache instance
    
    Automatically selects Redis if available and configured, otherwise falls back to in-memory.
    
    Args:
        ttl_days: Number of days to cache results (default: 7)
        redis_url: Redis connection URL (optional, will use from settings if not provided)
        
    Returns:
        Cache instance (Redis or InMemory)
    """
    global _cache_instance
    
    if _cache_instance is not None:
        return _cache_instance
    
    # Try to get Redis URL from settings if not provided
    if redis_url is None:
        try:
            from app.core.config import settings
            redis_url = settings.redis_url
        except:
            redis_url = None
    
    # Try to use Redis if available and configured
    if REDIS_AVAILABLE and redis_url:
        try:
            _cache_instance = RedisCache(redis_url=redis_url, ttl_days=ttl_days)
            logger.info("✅ Using Redis cache (persistent, shared)")
            return _cache_instance
        except Exception as e:
            logger.warning(f"⚠️  Failed to initialize Redis cache: {str(e)}")
            logger.warning("⚠️  Falling back to in-memory cache")
    
    # Fall back to in-memory cache
    _cache_instance = InMemoryCache(ttl_days=ttl_days)
    logger.info("✅ Using in-memory cache (non-persistent)")
    return _cache_instance


def clear_cache() -> int:
    """
    Clear the global cache
    
    Returns:
        Number of entries cleared
    """
    cache = get_cache()
    return cache.clear()


def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics from the global cache
    
    Returns:
        Cache statistics dictionary
    """
    cache = get_cache()
    return cache.get_stats()
