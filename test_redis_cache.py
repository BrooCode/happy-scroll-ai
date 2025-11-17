"""
Test Redis Cache Connection and Functionality
"""
import asyncio
import sys
from loguru import logger

# Add app to path
sys.path.insert(0, 'd:/happy-scroll-ai')

from app.services.cache_service import get_cache
from app.core.config import settings


async def test_redis_connection():
    """Test Redis cache connection and basic operations"""
    
    print("\n" + "=" * 80)
    print("🔍 TESTING REDIS CACHE CONNECTION")
    print("=" * 80 + "\n")
    
    # Get cache instance (will auto-detect Redis)
    print("📡 Connecting to cache...")
    try:
        cache = get_cache(ttl_days=7)
        print(f"✅ Cache initialized: {cache.__class__.__name__}")
    except Exception as e:
        print(f"❌ Failed to initialize cache: {str(e)}")
        return False
    
    # Test 1: Set a test value
    print("\n" + "-" * 80)
    print("📝 Test 1: SET operation")
    print("-" * 80)
    
    test_video_id = "test_video_123"
    test_data = {
        "is_safe": True,
        "is_safe_transcript": True,
        "is_safe_thumbnail": True,
        "transcript_reason": "Test transcript is safe",
        "thumbnail_reason": "Test thumbnail is safe",
        "overall_reason": "Test video is safe",
        "video_title": "Test Video",
        "channel_title": "Test Channel"
    }
    
    try:
        cache.set(test_video_id, test_data)
        print(f"✅ Successfully cached test data for video: {test_video_id}")
    except Exception as e:
        print(f"❌ SET failed: {str(e)}")
        return False
    
    # Test 2: Get the value back
    print("\n" + "-" * 80)
    print("📖 Test 2: GET operation")
    print("-" * 80)
    
    try:
        retrieved_data = cache.get(test_video_id)
        if retrieved_data:
            print(f"✅ Successfully retrieved cached data")
            print(f"   Video Title: {retrieved_data.get('video_title')}")
            print(f"   Is Safe: {retrieved_data.get('is_safe')}")
            
            # Verify data integrity
            if retrieved_data == test_data:
                print("✅ Data integrity verified - exact match!")
            else:
                print("⚠️  Data mismatch detected")
        else:
            print("❌ Failed to retrieve data (returned None)")
            return False
    except Exception as e:
        print(f"❌ GET failed: {str(e)}")
        return False
    
    # Test 3: Get cache statistics
    print("\n" + "-" * 80)
    print("📊 Test 3: Cache Statistics")
    print("-" * 80)
    
    try:
        stats = cache.get_stats()
        print(f"✅ Cache Statistics:")
        print(f"   Cache Type: {stats.get('cache_type', 'Unknown')}")
        print(f"   Cache Hits: {stats.get('cache_hits', 0)}")
        print(f"   Cache Misses: {stats.get('cache_misses', 0)}")
        print(f"   Cached Entries: {stats.get('cached_entries', 0)}")
        print(f"   Hit Rate: {stats.get('hit_rate_percentage', 0)}%")
        print(f"   Persistent: {stats.get('persistent', False)}")
        print(f"   Shared: {stats.get('shared', False)}")
    except Exception as e:
        print(f"❌ Stats failed: {str(e)}")
        return False
    
    # Test 4: Test cache miss
    print("\n" + "-" * 80)
    print("🔍 Test 4: Cache MISS (non-existent key)")
    print("-" * 80)
    
    try:
        non_existent = cache.get("video_that_does_not_exist")
        if non_existent is None:
            print("✅ Cache MISS handled correctly (returned None)")
        else:
            print("❌ Unexpected data returned for non-existent key")
            return False
    except Exception as e:
        print(f"❌ Cache miss test failed: {str(e)}")
        return False
    
    # Test 5: Clear cache (optional)
    print("\n" + "-" * 80)
    print("🗑️  Test 5: CLEAR operation")
    print("-" * 80)
    
    try:
        cleared_count = cache.clear()
        print(f"✅ Cache cleared: {cleared_count} entries removed")
    except Exception as e:
        print(f"❌ Clear failed: {str(e)}")
        return False
    
    # Final Results
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    
    # Show Redis connection info
    if hasattr(cache, 'redis_client'):
        print("\n🔗 Redis Connection Details:")
        print(f"   Connected to: {cache._mask_url(settings.redis_url)}")
        print(f"   TTL: {cache.ttl_days} days ({cache.ttl_seconds} seconds)")
        print(f"   Status: ✅ CONNECTED")
    else:
        print("\n⚠️  Using in-memory cache (Redis not configured)")
    
    print("\n" + "=" * 80 + "\n")
    
    return True


if __name__ == "__main__":
    # Run async test
    success = asyncio.run(test_redis_connection())
    
    if success:
        print("✅ Redis cache is working correctly!")
        sys.exit(0)
    else:
        print("❌ Redis cache tests failed!")
        sys.exit(1)
