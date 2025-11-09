"""
Quick script to test your OpenAI API key and check rate limits.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection and rate limits."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return
    
    print(f"✅ API Key found: {api_key[:20]}...{api_key[-4:]}")
    print("\nTesting OpenAI connection...")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Try a simple moderation request
        print("\n🔄 Attempting moderation request...")
        response = client.moderations.create(
            model="omni-moderation-latest",
            input="Hello, this is a test message."
        )
        
        print("✅ Success! Connection is working.")
        print(f"   Model used: omni-moderation-latest")
        print(f"   Flagged: {response.results[0].flagged}")
        
    except Exception as e:
        error_str = str(e)
        print(f"\n❌ Error: {error_str}")
        
        if "429" in error_str:
            print("\n🚨 Rate Limit Issue Detected!")
            print("\nPossible causes:")
            print("  1. Free tier rate limits exceeded")
            print("  2. Too many requests in short time")
            print("  3. Account needs billing setup")
            print("\n💡 Solutions:")
            print("  1. Wait 60 seconds and try again")
            print("  2. Check usage: https://platform.openai.com/account/usage")
            print("  3. Add payment method: https://platform.openai.com/account/billing")
            print("  4. Upgrade to paid tier for higher limits")
            
        elif "401" in error_str or "authentication" in error_str.lower():
            print("\n🚨 Authentication Issue!")
            print("  - Check if your API key is correct")
            print("  - Verify key hasn't expired")
            print("  - Get new key: https://platform.openai.com/api-keys")
            
        elif "model" in error_str.lower():
            print("\n🚨 Model Issue!")
            print("  - Trying fallback model...")
            try:
                response = client.moderations.create(
                    model="text-moderation-latest",
                    input="Hello, this is a test message."
                )
                print("✅ Fallback model works!")
                print(f"   Model used: text-moderation-latest")
            except Exception as fallback_error:
                print(f"❌ Fallback also failed: {fallback_error}")

if __name__ == "__main__":
    print("=" * 60)
    print("OpenAI API Connection Test")
    print("=" * 60)
    test_openai_connection()
    print("\n" + "=" * 60)
