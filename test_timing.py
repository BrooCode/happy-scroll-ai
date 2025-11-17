import requests
import time

BASE_URL = "http://localhost:8000"

def test_single_video_timing():
    """Test a single video and measure response time"""
    
    print("\n" + "="*80)
    print("⏱️  API Response Time Test")
    print("="*80)
    
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\n🎬 Testing video: {test_url}")
    print("📊 Measuring response time...\n")
    
    # Start timing
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/happyScroll/v1/verdict",
            json={"video_url": test_url},
            timeout=120
        )
        
        # End timing
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("="*80)
        print("⏱️  TIMING RESULTS")
        print("="*80)
        print(f"⏰ Total Response Time: {elapsed_time:.2f} seconds")
        print(f"⏰ Minutes: {elapsed_time/60:.2f} minutes")
        print("="*80)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Status: {response.status_code}")
            print(f"🎯 Overall Safe: {data['is_safe']}")
            print(f"📝 Transcript Safe: {data['is_safe_transcript']}")
            print(f"🖼️  Thumbnail Safe: {data['is_safe_thumbnail']}")
            print(f"📹 Video: {data['video_title']}")
            
            # Time breakdown estimate
            print("\n" + "="*80)
            print("⏱️  ESTIMATED BREAKDOWN")
            print("="*80)
            print("📝 Transcript Analysis: ~70-80% of total time")
            print("🖼️  Thumbnail Moderation: ~10-15% of total time")
            print("⚙️  Overhead (API calls, processing): ~5-15% of total time")
            print("="*80)
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Details: {response.text}")
            
    except requests.Timeout:
        print("❌ Request timed out (> 120 seconds)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "="*80)
    print("🏁 Test Complete")
    print("="*80)

if __name__ == "__main__":
    print("\n⚠️  Make sure the server is running: uvicorn app.main:app --reload")
    input("\nPress Enter to start the test...")
    test_single_video_timing()
