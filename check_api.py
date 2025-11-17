"""
Quick API Connection Test
Simply checks if the HappyScroll API is responding.
"""
import httpx
import json
import sys


def test_api_connection():
    """Test if API is responding and working."""
    
    api_url = "http://localhost:8000"
    
    print("=" * 60)
    print("  HappyScroll API Connection Test")
    print("=" * 60)
    print(f"\nTesting API at: {api_url}\n")
    
    # Test 1: Check if server is running
    print("1. Checking server connection...")
    try:
        response = httpx.get(f"{api_url}/", timeout=5.0)
        print(f"   ✓ Server is running (Status: {response.status_code})")
    except httpx.ConnectError:
        print(f"   ✗ ERROR: Cannot connect to {api_url}")
        print(f"   → Server is NOT running")
        print(f"   → Start it with: python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"   ✗ ERROR: {str(e)}")
        return False
    
    # Test 2: Health check
    print("\n2. Checking health endpoint...")
    try:
        response = httpx.get(f"{api_url}/api/health", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Health check passed")
            print(f"   → Status: {data.get('status', 'unknown')}")
        else:
            print(f"   ✗ Health check failed (Status: {response.status_code})")
    except Exception as e:
        print(f"   ✗ ERROR: {str(e)}")
    
    # Test 3: Moderation API
    print("\n3. Testing moderation endpoint...")
    try:
        test_payload = {
            "content": "Hello! This is a test message to check if moderation works."
        }
        
        response = httpx.post(
            f"{api_url}/api/moderate",
            json=test_payload,
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Moderation API is working!")
            print(f"   → Content allowed: {data.get('allowed', data.get('safe', 'unknown'))}")
            
            if 'categories' in data:
                flagged = [k for k, v in data.get('categories', {}).items() if v]
                if flagged:
                    print(f"   → Flagged categories: {flagged}")
                else:
                    print(f"   → No concerning content detected")
            
            print("\n" + "=" * 60)
            print("  ✓ API IS WORKING CORRECTLY!")
            print("=" * 60)
            
            print("\n📊 Full Response:")
            print(json.dumps(data, indent=2))
            return True
            
        elif response.status_code == 429:
            print(f"   ✗ Rate limit exceeded (429)")
            print(f"   → OpenAI API rate limit hit")
            print(f"   → Wait 60 seconds and try again")
            print(f"   → Or check: https://platform.openai.com/account/usage")
            
            try:
                error_data = response.json()
                print(f"\n   Error details: {error_data.get('detail', 'Unknown')}")
            except:
                pass
            return False
            
        elif response.status_code == 500:
            print(f"   ✗ Server error (500)")
            try:
                error_data = response.json()
                print(f"   → {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   → {response.text}")
            return False
            
        else:
            print(f"   ✗ Unexpected response (Status: {response.status_code})")
            print(f"   → {response.text}")
            return False
            
    except httpx.TimeoutException:
        print(f"   ✗ Request timed out (took > 30 seconds)")
        print(f"   → OpenAI API might be slow or rate limited")
        return False
    except Exception as e:
        print(f"   ✗ ERROR: {str(e)}")
        return False


if __name__ == "__main__":
    try:
        success = test_api_connection()
        print()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
