"""
Quick Redis Connection Test
"""
import redis

# Your Redis connection string
redis_url = "redis://default:Jvd6exTZVwCAr5To63DjxkE3dCPrOkg8@redis-17747.c232.us-east-1-2.ec2.cloud.redislabs.com:17747"

print("=" * 80)
print("Testing Redis Connection...")
print("=" * 80)

try:
    # Create Redis client
    client = redis.from_url(redis_url, decode_responses=True)
    
    # Test PING
    print("\n1. Testing PING...")
    response = client.ping()
    print(f"   ✅ PING response: {response}")
    
    # Test SET
    print("\n2. Testing SET...")
    client.set("test_key", "Hello Redis!", ex=60)
    print("   ✅ SET successful")
    
    # Test GET
    print("\n3. Testing GET...")
    value = client.get("test_key")
    print(f"   ✅ GET successful: {value}")
    
    # Test DEL
    print("\n4. Testing DEL...")
    client.delete("test_key")
    print("   ✅ DELETE successful")
    
    print("\n" + "=" * 80)
    print("✅ ALL REDIS TESTS PASSED!")
    print("=" * 80)
    print("\nYour Redis server is working correctly!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nConnection failed. Please check:")
    print("  1. Redis URL is correct")
    print("  2. Redis server is running")
    print("  3. Firewall allows connections")
