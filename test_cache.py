"""
Test Cache Functionality - Demonstrates Speed Improvement
Shows the difference between first request (slow) and cached request (instant)
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_cache_performance():
    """Test cache performance with same video twice"""
    
    print("\n" + "="*80)
    print("⚡ CACHE PERFORMANCE TEST")
    print("="*80)
    
    test_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n🎬 Test Video: {test_video}")
    print("\n" + "="*80)
    print("TEST 1: First Request (No Cache - Full Analysis)")
    print("="*80)
    
    # First request - will be slow (full analysis)
    print("\n⏳ Sending first request...")
    start_time = time.time()
    
    try:
        response1 = requests.post(
            f"{BASE_URL}/api/happyScroll/v1/verdict",
            json={"video_url": test_video},
            timeout=120
        )
        
        elapsed1 = time.time() - start_time
        
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"\n✅ Response received!")
            print(f"⏰ Time: {elapsed1:.2f} seconds")
            print(f"🎯 Safe: {data1['is_safe']}")
            print(f"📹 Video: {data1['video_title']}")
        else:
            print(f"❌ Error: {response1.status_code}")
            return
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Wait a moment
    print("\n⏸️  Waiting 2 seconds before second request...")
    time.sleep(2)
    
    print("\n" + "="*80)
    print("TEST 2: Second Request (WITH Cache - Should be instant!)")
    print("="*80)
    
    # Second request - should be instant (cached)
    print("\n⚡ Sending second request (same video)...")
    start_time = time.time()
    
    try:
        response2 = requests.post(
            f"{BASE_URL}/api/happyScroll/v1/verdict",
            json={"video_url": test_video},
            timeout=120
        )
        
        elapsed2 = time.time() - start_time
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"\n✅ Response received!")
            print(f"⏰ Time: {elapsed2:.2f} seconds")
            print(f"🎯 Safe: {data2['is_safe']}")
            print(f"📹 Video: {data2['video_title']}")
        else:
            print(f"❌ Error: {response2.status_code}")
            return
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Calculate improvement
    print("\n" + "="*80)
    print("📊 PERFORMANCE COMPARISON")
    print("="*80)
    
    time_saved = elapsed1 - elapsed2
    percent_faster = (time_saved / elapsed1) * 100 if elapsed1 > 0 else 0
    
    print(f"\n1️⃣  First Request (No Cache):  {elapsed1:.2f}s")
    print(f"2️⃣  Second Request (Cached):   {elapsed2:.2f}s")
    print(f"⚡ Time Saved:                 {time_saved:.2f}s")
    print(f"🚀 Speed Improvement:          {percent_faster:.0f}% faster!")
    
    if elapsed2 < 1:
        print(f"\n✅ SUCCESS: Cache is working perfectly!")
        print(f"   Second request was {elapsed1/elapsed2:.0f}x faster!")
    elif elapsed2 < 2:
        print(f"\n✅ GOOD: Cache is working well!")
    else:
        print(f"\n⚠️  WARNING: Second request should be <1s if cached")
    
    # Get cache statistics
    print("\n" + "="*80)
    print("📊 CACHE STATISTICS")
    print("="*80)
    
    try:
        stats_response = requests.get(f"{BASE_URL}/api/happyScroll/v1/cache/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()["cache_statistics"]
            
            print(f"\n📈 Cache Performance:")
            print(f"   Total Requests:    {stats['total_requests']}")
            print(f"   Cache Hits:        {stats['cache_hits']}")
            print(f"   Cache Misses:      {stats['cache_misses']}")
            print(f"   Hit Rate:          {stats['hit_rate_percentage']}%")
            print(f"   Cached Entries:    {stats['cached_entries']}")
            print(f"\n⏰ Time Savings:")
            print(f"   Seconds Saved:     {stats['time_saved_seconds']}s")
            print(f"   Minutes Saved:     {stats['time_saved_minutes']} min")
            print(f"   Cost Saved:        ${stats['estimated_cost_saved_usd']}")
            print(f"\n⚙️  Cache Settings:")
            print(f"   TTL:               {stats['ttl_days']} days")
    except Exception as e:
        print(f"⚠️  Could not fetch cache statistics: {str(e)}")
    
    print("\n" + "="*80)
    print("🎯 CACHE TEST COMPLETE!")
    print("="*80)
    print("\n💡 Key Takeaways:")
    print("   ✅ First request performs full analysis (slow)")
    print("   ✅ Subsequent requests use cache (instant!)")
    print("   ✅ Cache expires after 7 days")
    print("   ✅ Popular videos will almost always be cached")
    print("\n" + "="*80)

def test_multiple_videos():
    """Test cache with multiple different videos"""
    
    print("\n" + "="*80)
    print("⚡ MULTIPLE VIDEOS CACHE TEST")
    print("="*80)
    
    videos = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "https://www.youtube.com/shorts/JkV-BbqA6L0"
    ]
    
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*80}")
        print(f"Video {i}/{len(videos)}: {video}")
        print(f"{'='*80}")
        
        # First request
        print("\n⏳ First request (full analysis)...")
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/happyScroll/v1/verdict",
                json={"video_url": video},
                timeout=120
            )
            
            elapsed_first = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Complete: {elapsed_first:.2f}s - Safe: {data['is_safe']}")
            else:
                print(f"❌ Error: {response.status_code}")
                continue
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue
        
        # Wait a moment
        time.sleep(1)
        
        # Second request (cached)
        print("⚡ Second request (cached)...")
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/happyScroll/v1/verdict",
                json={"video_url": video},
                timeout=120
            )
            
            elapsed_cached = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✅ Complete: {elapsed_cached:.2f}s ({elapsed_first/elapsed_cached:.0f}x faster!)")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Final stats
    print("\n" + "="*80)
    print("📊 FINAL CACHE STATISTICS")
    print("="*80)
    
    try:
        stats_response = requests.get(f"{BASE_URL}/api/happyScroll/v1/cache/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()["cache_statistics"]
            print(f"\nCache Performance: {stats['hit_rate_percentage']}% hit rate")
            print(f"Time Saved: {stats['time_saved_minutes']} minutes")
            print(f"Cached Videos: {stats['cached_entries']}")
    except:
        pass
    
    print("\n" + "="*80)

if __name__ == "__main__":
    print("\n⚠️  PREREQUISITES:")
    print("   1. Server must be running: uvicorn app.main:app --reload")
    print("   2. All API keys must be configured")
    
    print("\n📋 TEST OPTIONS:")
    print("   1. Single video test (shows cache speed improvement)")
    print("   2. Multiple videos test (builds up cache)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_cache_performance()
    elif choice == "2":
        test_multiple_videos()
    else:
        print("Invalid choice. Running single video test...")
        test_cache_performance()
