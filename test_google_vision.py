"""
Quick test script for Google Cloud Vision API integration.
Run this to verify your Google Cloud credentials and Vision API setup.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.google_vision_service import GoogleVisionService
from app.core.config import get_settings


async def test_google_vision():
    """Test Google Cloud Vision API integration."""
    
    print("=" * 60)
    print("🔍 Testing Google Cloud Vision API Integration")
    print("=" * 60)
    
    # Check environment variables
    print("\n📋 Step 1: Checking environment variables...")
    settings = get_settings()
    
    credentials_path = settings.google_application_credentials
    project_id = settings.google_cloud_project
    threshold = settings.safety_threshold
    
    print(f"   Credentials path: {credentials_path}")
    print(f"   Project ID: {project_id}")
    print(f"   Safety threshold: {threshold}")
    
    # Check if credentials file exists
    if not os.path.exists(credentials_path):
        print(f"\n❌ ERROR: Credentials file not found at: {credentials_path}")
        print("\nPlease follow these steps:")
        print("1. Create a Google Cloud project")
        print("2. Enable Vision API")
        print("3. Create service account and download JSON key")
        print("4. Update GOOGLE_APPLICATION_CREDENTIALS in .env file")
        print("\nSee GOOGLE_CLOUD_SETUP.md for detailed instructions.")
        return False
    
    print("   ✅ Credentials file found")
    
    # Initialize Vision service
    print("\n🚀 Step 2: Initializing Google Vision service...")
    try:
        service = GoogleVisionService(
            credentials_path=credentials_path,
            project_id=project_id,
            safety_threshold=threshold
        )
        print("   ✅ Service initialized successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize service: {e}")
        return False
    
    # Test with safe images
    print("\n🖼️  Step 3: Testing SafeSearch with safe images...")
    
    test_images = [
        {
            "name": "Google Doves (Safe)",
            "url": "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Dove_2880p_001.width-1300.jpg",
            "expected_safe": True
        },
        {
            "name": "YouTube Safe Thumbnail",
            "url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
            "expected_safe": True
        }
    ]
    
    all_passed = True
    
    for test_image in test_images:
        print(f"\n   Testing: {test_image['name']}")
        print(f"   URL: {test_image['url']}")
        
        try:
            # Test is_safe_content
            is_safe = await service.is_safe_content(test_image['url'])
            print(f"   Result: {'✅ SAFE' if is_safe else '❌ UNSAFE'}")
            
            if is_safe != test_image['expected_safe']:
                print(f"   ⚠️  Expected: {test_image['expected_safe']}, Got: {is_safe}")
                all_passed = False
            
            # Test detailed analysis
            analysis = await service.analyze_content(test_image['url'])
            print(f"   Categories:")
            for category, likelihood in analysis['likelihood_scores'].items():
                safe_icon = "✅" if not analysis['categories'][category] else "⚠️"
                print(f"      {safe_icon} {category}: {likelihood}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Google Cloud Vision is working correctly.")
        print("\nYou can now:")
        print("1. Start the API server: python -m uvicorn app.main:app --reload")
        print("2. Test the API: http://localhost:8000/docs")
        print("3. Integrate with your Chrome extension")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify Google Cloud credentials are correct")
        print("2. Check Vision API is enabled in your project")
        print("3. Ensure service account has proper permissions")
        print("\nSee GOOGLE_CLOUD_SETUP.md for help.")
    print("=" * 60)
    
    return all_passed


async def test_video_service():
    """Test Google Video Intelligence API (optional)."""
    print("\n\n🎬 Optional: Testing Video Intelligence API...")
    print("Note: Video analysis is slow (1-5 minutes) and expensive.")
    print("Skipping video test. To enable, uncomment the code in this script.")
    
    # Uncomment to test video analysis:
    # from app.services.google_video_service import GoogleVideoService
    # settings = get_settings()
    # video_service = GoogleVideoService(
    #     credentials_path=settings.google_application_credentials,
    #     project_id=settings.google_cloud_project
    # )
    # result = await video_service.quick_video_check("gs://your-bucket/video.mp4")
    # print(f"Video safe: {result['is_safe']}")


if __name__ == "__main__":
    print("\n🧪 Google Cloud Vision API Test Script\n")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ ERROR: .env file not found!")
        print("\nPlease create a .env file with:")
        print("   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json")
        print("   GOOGLE_CLOUD_PROJECT=your-project-id")
        print("   SAFETY_THRESHOLD=POSSIBLE")
        print("\nSee GOOGLE_CLOUD_SETUP.md for detailed instructions.")
        sys.exit(1)
    
    # Run tests
    try:
        result = asyncio.run(test_google_vision())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
