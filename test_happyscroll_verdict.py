"""
Test script for HappyScroll Combined Verdict API.
Tests the /api/happyScroll/v1/verdict endpoint.
"""
import requests
import json


def test_happyscroll_verdict():
    """Test the combined verdict endpoint with various videos."""
    
    print("=" * 80)
    print("Testing HappyScroll Combined Verdict API")
    print("=" * 80)
    
    base_url = "http://localhost:8000/api/happyScroll/v1/verdict"
    
    # Test cases
    test_cases = [
        {
            "name": "Safe Educational Video",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "expected": "Should be safe (both transcript and thumbnail)"
        },
        {
            "name": "YouTube Shorts",
            "url": "https://www.youtube.com/shorts/JkV-BbqA6L0",
            "expected": "Check if safe or unsafe"
        },
        {
            "name": "Shortened URL",
            "url": "https://youtu.be/dQw4w9WgXcQ",
            "expected": "Should handle shortened URLs"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {i}: {test['name']}")
        print(f"URL: {test['url']}")
        print(f"Expected: {test['expected']}")
        print("=" * 80)
        
        try:
            print(f"\n🔄 Sending request to {base_url}...")
            
            response = requests.post(
                base_url,
                json={"video_url": test["url"]},
                timeout=60  # Combined analysis takes longer
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n{'='*80}")
                print("✅ RESPONSE RECEIVED")
                print("=" * 80)
                
                # Overall Verdict
                print(f"\n🎯 OVERALL VERDICT:")
                print(f"   is_safe: {data['is_safe']}")
                status_icon = "✅" if data['is_safe'] else "❌"
                print(f"   Status: {status_icon} {'SAFE' if data['is_safe'] else 'UNSAFE'}")
                print(f"   Reason: {data['overall_reason']}")
                
                # Transcript Analysis
                print(f"\n📝 TRANSCRIPT ANALYSIS:")
                print(f"   is_safe_transcript: {data['is_safe_transcript']}")
                transcript_icon = "✅" if data['is_safe_transcript'] else "❌"
                print(f"   Status: {transcript_icon}")
                print(f"   Reason: {data['transcript_reason'][:150]}...")
                
                # Thumbnail Moderation
                print(f"\n🖼️  THUMBNAIL MODERATION:")
                print(f"   is_safe_thumbnail: {data['is_safe_thumbnail']}")
                thumbnail_icon = "✅" if data['is_safe_thumbnail'] else "❌"
                print(f"   Status: {thumbnail_icon}")
                print(f"   Reason: {data['thumbnail_reason']}")
                
                # Video Info
                print(f"\n📹 VIDEO INFORMATION:")
                print(f"   Title: {data.get('video_title', 'N/A')}")
                print(f"   Channel: {data.get('channel_title', 'N/A')}")
                
                # Test Result
                print(f"\n{'='*80}")
                if data['is_safe']:
                    print("✅ TEST RESULT: Video marked as SAFE")
                else:
                    print("❌ TEST RESULT: Video marked as UNSAFE")
                print("=" * 80)
                
            else:
                print(f"\n❌ ERROR Response:")
                print(f"Status: {response.status_code}")
                print(f"Body: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ERROR: Could not connect to server")
            print(f"   Make sure the server is running:")
            print(f"   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            break
        except requests.exceptions.Timeout:
            print(f"\n⏱️  ERROR: Request timed out (analysis takes 30-60 seconds)")
            print(f"   This is normal for the first request or complex videos")
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
    
    print(f"\n{'='*80}")
    print("Testing Complete")
    print("=" * 80)


def test_error_cases():
    """Test error handling."""
    
    print("\n" + "=" * 80)
    print("Testing Error Cases")
    print("=" * 80)
    
    base_url = "http://localhost:8000/api/happyScroll/v1/verdict"
    
    error_tests = [
        {
            "name": "Empty URL",
            "payload": {"video_url": ""},
            "expected_status": 400
        },
        {
            "name": "Invalid URL (not YouTube)",
            "payload": {"video_url": "https://www.example.com/video"},
            "expected_status": 400
        },
        {
            "name": "No video_url field",
            "payload": {},
            "expected_status": 422
        }
    ]
    
    for test in error_tests:
        print(f"\n{test['name']}:")
        try:
            response = requests.post(
                base_url,
                json=test["payload"],
                timeout=10
            )
            
            print(f"  Status: {response.status_code} (Expected: {test['expected_status']})")
            
            if response.status_code == test['expected_status']:
                print(f"  ✅ Correct error handling")
            else:
                print(f"  ⚠️  Unexpected status code")
            
            if response.status_code >= 400:
                error_detail = response.json().get('detail', 'N/A')
                print(f"  Error: {error_detail}")
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")


def compare_with_individual_endpoints():
    """Compare combined endpoint with individual API calls."""
    
    print("\n" + "=" * 80)
    print("Comparing Combined vs Individual Endpoints")
    print("=" * 80)
    
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"\nTest Video: {test_url}")
    
    # Test combined endpoint
    print("\n1️⃣  Testing Combined Endpoint (/api/happyScroll/v1/verdict):")
    try:
        combined_response = requests.post(
            "http://localhost:8000/api/happyScroll/v1/verdict",
            json={"video_url": test_url},
            timeout=60
        )
        
        if combined_response.status_code == 200:
            combined_data = combined_response.json()
            print(f"   ✅ Success")
            print(f"   Overall Safe: {combined_data['is_safe']}")
            print(f"   Transcript Safe: {combined_data['is_safe_transcript']}")
            print(f"   Thumbnail Safe: {combined_data['is_safe_thumbnail']}")
        else:
            print(f"   ❌ Error: {combined_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test individual endpoints
    print("\n2️⃣  Testing Individual Endpoints:")
    
    print("   📝 /api/analyze_video:")
    try:
        analyze_response = requests.post(
            "http://localhost:8000/api/analyze_video",
            json={"video_url": test_url},
            timeout=60
        )
        
        if analyze_response.status_code == 200:
            analyze_data = analyze_response.json()
            print(f"      ✅ Success - Safe: {analyze_data['is_safe']}")
        else:
            print(f"      ❌ Error: {analyze_response.status_code}")
    except Exception as e:
        print(f"      ❌ Error: {str(e)}")
    
    print("   🖼️  /api/moderate:")
    try:
        moderate_response = requests.post(
            "http://localhost:8000/api/moderate",
            json={"youtube_url": test_url},
            timeout=30
        )
        
        if moderate_response.status_code == 200:
            moderate_data = moderate_response.json()
            print(f"      ✅ Success - Safe: {moderate_data['safe']}")
        else:
            print(f"      ❌ Error: {moderate_response.status_code}")
    except Exception as e:
        print(f"      ❌ Error: {str(e)}")
    
    print(f"\n✅ Combined endpoint provides both results in a single call!")


if __name__ == "__main__":
    print("\n" + "🎯" * 40)
    print("HappyScroll Combined Verdict API - Test Suite")
    print("🎯" * 40 + "\n")
    
    print("⚠️  NOTE: This test takes 30-60 seconds per video as it performs:")
    print("   1. Video transcript analysis with Gemini AI")
    print("   2. Thumbnail moderation with Google Cloud Vision")
    print("   3. Combined verdict generation")
    print()
    
    # Run tests
    test_happyscroll_verdict()
    test_error_cases()
    compare_with_individual_endpoints()
    
    print("\n" + "🎉" * 40)
    print("All Tests Complete!")
    print("🎉" * 40 + "\n")
