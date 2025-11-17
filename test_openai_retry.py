"""
OpenAI API Test with Retry
Waits and retries if rate limited.
"""
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_with_retry():
    """Test OpenAI API with retry logic."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return False
    
    print("=" * 60)
    print("  OpenAI API Test (with Retry)")
    print("=" * 60)
    print(f"\n✅ API Key found: {api_key[:20]}...{api_key[-4:]}\n")
    
    client = OpenAI(api_key=api_key)
    max_retries = 3
    
    for attempt in range(1, max_retries + 1):
        print(f"🔄 Attempt {attempt}/{max_retries}...")
        
        try:
            response = client.moderations.create(
                model="omni-moderation-latest",
                input="Hello, this is a test message."
            )
            
            print("✅ SUCCESS! OpenAI API is working!\n")
            print(f"   Model: omni-moderation-latest")
            print(f"   Flagged: {response.results[0].flagged}")
            print(f"   Response ID: {response.id}\n")
            print("=" * 60)
            print("  ✓ YOUR OPENAI API IS WORKING CORRECTLY!")
            print("=" * 60)
            return True
            
        except Exception as e:
            error_str = str(e)
            
            if "429" in error_str:
                print(f"⚠️  Rate limited (429)\n")
                
                if attempt < max_retries:
                    wait_time = 30 * attempt  # 30s, 60s, 90s
                    print(f"   Waiting {wait_time} seconds before retry...")
                    print(f"   (You can press Ctrl+C to cancel)\n")
                    
                    try:
                        time.sleep(wait_time)
                    except KeyboardInterrupt:
                        print("\n\n❌ Test cancelled by user.")
                        return False
                else:
                    print("❌ Still rate limited after all retries\n")
                    print("📋 Next Steps:")
                    print("   1. Wait 5-10 minutes")
                    print("   2. Check usage: https://platform.openai.com/account/usage")
                    print("   3. Add payment: https://platform.openai.com/account/billing")
                    return False
            else:
                print(f"❌ Error: {error_str}\n")
                return False
    
    return False

if __name__ == "__main__":
    print("\nThis will test your OpenAI API and retry if rate limited.\n")
    
    try:
        success = test_with_retry()
        print()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled.\n")
        exit(1)
