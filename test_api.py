"""
HappyScroll API Test Script
Tests all endpoints and validates the moderation API functionality.
"""
import sys
import time
import httpx
from typing import Dict, Any


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class APITester:
    """Test suite for HappyScroll Moderation API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)
        self.tests_passed = 0
        self.tests_failed = 0
    
    def print_header(self, text: str):
        """Print a formatted header."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.END}\n")
    
    def print_test(self, name: str):
        """Print test name."""
        print(f"{Colors.BLUE}▶ Testing: {Colors.END}{name}")
    
    def print_success(self, message: str):
        """Print success message."""
        self.tests_passed += 1
        print(f"  {Colors.GREEN}✓ {message}{Colors.END}")
    
    def print_error(self, message: str):
        """Print error message."""
        self.tests_failed += 1
        print(f"  {Colors.RED}✗ {message}{Colors.END}")
    
    def print_warning(self, message: str):
        """Print warning message."""
        print(f"  {Colors.YELLOW}⚠ {message}{Colors.END}")
    
    def print_info(self, message: str):
        """Print info message."""
        print(f"  {Colors.CYAN}ℹ {message}{Colors.END}")
    
    def test_server_reachable(self) -> bool:
        """Test if server is reachable."""
        self.print_test("Server Connectivity")
        try:
            response = self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.print_success(f"Server is reachable at {self.base_url}")
                return True
            else:
                self.print_error(f"Server returned status code: {response.status_code}")
                return False
        except httpx.ConnectError:
            self.print_error(f"Cannot connect to server at {self.base_url}")
            self.print_warning("Make sure the server is running with: python -m uvicorn app.main:app --reload")
            return False
        except Exception as e:
            self.print_error(f"Connection error: {str(e)}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint."""
        self.print_test("Root Endpoint (GET /)")
        try:
            response = self.client.get(f"{self.base_url}/")
            data = response.json()
            
            if response.status_code == 200:
                self.print_success("Root endpoint responding")
                if "name" in data and "HappyScroll" in data["name"]:
                    self.print_success(f"API Name: {data['name']}")
                if "version" in data:
                    self.print_success(f"Version: {data['version']}")
                if "status" in data:
                    self.print_success(f"Status: {data['status']}")
                return True
            else:
                self.print_error(f"Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def test_health_endpoint(self) -> bool:
        """Test the health check endpoint."""
        self.print_test("Health Check Endpoint (GET /api/health)")
        try:
            response = self.client.get(f"{self.base_url}/api/health")
            data = response.json()
            
            if response.status_code == 200:
                self.print_success("Health endpoint responding")
                if data.get("status") == "healthy":
                    self.print_success("Server status: Healthy")
                if "service" in data:
                    self.print_success(f"Service: {data['service']}")
                return True
            else:
                self.print_error(f"Health check failed with status: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def test_moderation_safe_content(self) -> bool:
        """Test moderation with safe content."""
        self.print_test("Moderation API - Safe Content (POST /api/moderate)")
        try:
            payload = {"content": "Hello! This is a friendly and safe message."}
            response = self.client.post(
                f"{self.base_url}/api/moderate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Moderation endpoint responding")
                
                # Check response structure
                if "allowed" in data:
                    self.print_success(f"Content allowed: {data['allowed']}")
                else:
                    self.print_warning("Response missing 'allowed' field")
                
                if "safe" in data:
                    self.print_success(f"Content safe: {data['safe']}")
                
                if "categories" in data:
                    self.print_success(f"Categories returned: {len(data['categories'])} categories")
                    flagged = [k for k, v in data['categories'].items() if v]
                    if flagged:
                        self.print_warning(f"Flagged categories: {flagged}")
                    else:
                        self.print_success("No categories flagged (as expected)")
                
                if "category_scores" in data:
                    self.print_success("Category scores included")
                
                return data.get("allowed", False) or data.get("safe", False)
            elif response.status_code == 429:
                data = response.json()
                self.print_error("Rate limit exceeded (429)")
                self.print_warning("Your OpenAI API has hit rate limits")
                self.print_info("Solutions:")
                self.print_info("  1. Wait 60-120 seconds and try again")
                self.print_info("  2. Check usage: https://platform.openai.com/account/usage")
                self.print_info("  3. Add payment method: https://platform.openai.com/account/billing")
                return False
            elif response.status_code == 500:
                data = response.json()
                self.print_error("Server error (500)")
                self.print_warning(f"Details: {data.get('detail', 'Unknown error')}")
                if "OpenAI" in str(data):
                    self.print_info("This appears to be an OpenAI API issue")
                return False
            else:
                self.print_error(f"Unexpected status code: {response.status_code}")
                self.print_info(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def test_moderation_empty_content(self) -> bool:
        """Test moderation with empty content."""
        self.print_test("Moderation API - Empty Content Validation")
        try:
            payload = {"content": ""}
            response = self.client.post(
                f"{self.base_url}/api/moderate",
                json=payload
            )
            
            if response.status_code == 400:
                self.print_success("Empty content properly rejected (400)")
                return True
            else:
                self.print_warning(f"Expected 400, got {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def test_moderation_missing_content(self) -> bool:
        """Test moderation with missing content field."""
        self.print_test("Moderation API - Missing Content Field")
        try:
            payload = {}
            response = self.client.post(
                f"{self.base_url}/api/moderate",
                json=payload
            )
            
            if response.status_code == 422:
                self.print_success("Missing content field properly rejected (422)")
                return True
            else:
                self.print_warning(f"Expected 422, got {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def test_docs_endpoint(self) -> bool:
        """Test if API documentation is accessible."""
        self.print_test("API Documentation (GET /docs)")
        try:
            response = self.client.get(f"{self.base_url}/docs")
            
            if response.status_code == 200:
                self.print_success("Swagger UI documentation is accessible")
                self.print_info(f"Visit: {self.base_url}/docs")
                return True
            else:
                self.print_error(f"Documentation returned status: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def test_openapi_schema(self) -> bool:
        """Test if OpenAPI schema is available."""
        self.print_test("OpenAPI Schema (GET /openapi.json)")
        try:
            response = self.client.get(f"{self.base_url}/openapi.json")
            
            if response.status_code == 200:
                schema = response.json()
                self.print_success("OpenAPI schema is accessible")
                if "info" in schema:
                    self.print_success(f"API Title: {schema['info'].get('title')}")
                    self.print_success(f"API Version: {schema['info'].get('version')}")
                return True
            else:
                self.print_error(f"Schema returned status: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all test cases."""
        self.print_header("HappyScroll Moderation API Test Suite")
        
        print(f"{Colors.CYAN}Testing API at: {Colors.BOLD}{self.base_url}{Colors.END}\n")
        
        # Test 1: Server connectivity
        if not self.test_server_reachable():
            self.print_header("TEST SUITE ABORTED")
            print(f"{Colors.RED}Cannot proceed without server connection{Colors.END}\n")
            return False
        
        print()  # Blank line
        
        # Test 2-3: Basic endpoints
        self.test_root_endpoint()
        print()
        
        self.test_health_endpoint()
        print()
        
        # Test 4-6: Moderation API
        self.test_moderation_safe_content()
        print()
        
        self.test_moderation_empty_content()
        print()
        
        self.test_moderation_missing_content()
        print()
        
        # Test 7-8: Documentation
        self.test_docs_endpoint()
        print()
        
        self.test_openapi_schema()
        print()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        
        self.print_header("Test Summary")
        
        print(f"Total Tests: {Colors.BOLD}{total}{Colors.END}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.END}")
        
        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED! API is working correctly.{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}⚠ Some tests failed. Check the details above.{Colors.END}\n")
        
        # Success rate
        success_rate = (self.tests_passed / total * 100) if total > 0 else 0
        print(f"Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.END}\n")


def main():
    """Main function to run tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test HappyScroll Moderation API")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    tester = APITester(base_url=args.url)
    tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if tester.tests_failed == 0 else 1)


if __name__ == "__main__":
    main()
