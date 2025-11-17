"""
Test script for YouTube moderation feature.
Run this after starting the server with: uvicorn app.main:app --reload
"""
import requests
import json


def test_youtube_moderation():
    """Test YouTube video moderation endpoint."""
    
    print("=" * 60)
    print("Testing YouTube Moderation Feature")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "name": "Rick Astley - Never Gonna Give You Up",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "expected": "safe"
        },
        {
            "name": "YouTube Shorts Example",
            "url": "https://www.youtube.com/shorts/JkV-BbqA6L0",
            "expected": "check"
        },
        {
            "name": "Shortened URL",
            "url": "https://youtu.be/dQw4w9WgXcQ",
            "expected": "safe"
        }
    ]
    
    base_url = "http://localhost:8000/api/moderate"
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test['name']}")
        print(f"URL: {test['url']}")
        print(f"Expected: {test['expected']}")
        print("=" * 60)
        
        try:
            response = requests.post(
                base_url,
                json={"youtube_url": test["url"]},
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n✅ Response:")
                print(f"  Safe: {data['safe']}")
                print(f"  Allowed: {data['allowed']}")
                print(f"  Reason: {data['reason']}")
                print(f"\n📹 Video Info:")
                print(f"  Title: {data.get('video_title', 'N/A')}")
                print(f"  Channel: {data.get('channel_title', 'N/A')}")
                print(f"  Thumbnail: {data.get('thumbnail_url', 'N/A')}")
                print(f"\n🔍 Categories:")
                for category, flagged in data['categories'].items():
                    status = "❌ FLAGGED" if flagged else "✅ Safe"
                    score = data['likelihood_scores'].get(category, 'N/A')
                    print(f"  {category.capitalize()}: {status} ({score})")
                
                # Check result
                if test['expected'] == 'safe' and data['safe']:
                    print(f"\n✅ TEST PASSED: Content correctly marked as safe")
                elif test['expected'] == 'unsafe' and not data['safe']:
                    print(f"\n✅ TEST PASSED: Content correctly marked as unsafe")
                else:
                    print(f"\n⚠️ TEST RESULT: Check manually")
                
            else:
                print(f"❌ Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ ERROR: Could not connect to server")
            print(f"   Make sure the server is running:")
            print(f"   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            break
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    print(f"\n{'='*60}")
    print("Testing Complete")
    print("=" * 60)


def test_direct_image():
    """Test direct image moderation (original functionality)."""
    
    print("\n" + "=" * 60)
    print("Testing Direct Image Moderation (Original Feature)")
    print("=" * 60)
    
    test_url = "https://picsum.photos/800/600"
    
    try:
        response = requests.post(
            "http://localhost:8000/api/moderate",
            json={"image_url": test_url},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Response:")
            print(f"  Safe: {data['safe']}")
            print(f"  Reason: {data['reason']}")
            print(f"  Service: {data['service']}")
            print(f"\n✅ Direct image moderation still works!")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def test_error_cases():
    """Test error handling."""
    
    print("\n" + "=" * 60)
    print("Testing Error Cases")
    print("=" * 60)
    
    error_tests = [
        {
            "name": "No URL provided",
            "payload": {},
            "expected_status": 422
        },
        {
            "name": "Both URLs provided",
            "payload": {
                "image_url": "https://example.com/image.jpg",
                "youtube_url": "https://www.youtube.com/watch?v=test"
            },
            "expected_status": 400
        },
        {
            "name": "Invalid YouTube URL",
            "payload": {
                "youtube_url": "https://www.youtube.com/playlist?list=123"
            },
            "expected_status": 400
        }
    ]
    
    for test in error_tests:
        print(f"\n{test['name']}:")
        try:
            response = requests.post(
                "http://localhost:8000/api/moderate",
                json=test["payload"],
                timeout=10
            )
            
            print(f"  Status: {response.status_code} (Expected: {test['expected_status']})")
            
            if response.status_code == test['expected_status']:
                print(f"  ✅ Correct error handling")
            else:
                print(f"  ⚠️ Unexpected status code")
            
            if response.status_code >= 400:
                print(f"  Error: {response.json().get('detail', 'N/A')}")
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("YouTube Moderation Feature - Test Suite")
    print("🚀" * 30 + "\n")
    
    # Run tests
    test_youtube_moderation()
    test_direct_image()
    test_error_cases()
    
    print("\n" + "🎉" * 30)
    print("All Tests Complete!")
    print("🎉" * 30 + "\n")
