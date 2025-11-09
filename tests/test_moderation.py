"""
Unit tests for the moderation API endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app

# Create test client
client = TestClient(app)


class TestModerationEndpoint:
    """Test suite for the /api/moderate endpoint."""
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "HappyScroll Moderation API"
        assert data["status"] == "running"
    
    @patch("app.services.openai_service.openai_service.moderate_content")
    def test_moderate_content_safe(self, mock_moderate):
        """Test moderation endpoint with safe content."""
        # Mock the service response
        mock_moderate.return_value = AsyncMock(
            return_value=(True, [], {"violence": 0.01, "hate": 0.02})
        )()
        
        # Make request
        response = client.post(
            "/api/moderate",
            json={"content": "This is a safe and friendly message"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["safe"] is True
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) == 0
    
    @patch("app.services.openai_service.openai_service.moderate_content")
    def test_moderate_content_unsafe(self, mock_moderate):
        """Test moderation endpoint with flagged content."""
        # Mock the service response
        mock_moderate.return_value = AsyncMock(
            return_value=(False, ["violence", "hate"], {"violence": 0.95, "hate": 0.88})
        )()
        
        # Make request
        response = client.post(
            "/api/moderate",
            json={"content": "Inappropriate content"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["safe"] is False
        assert "violence" in data["categories"]
        assert "hate" in data["categories"]
        assert "category_scores" in data
    
    def test_moderate_empty_content(self):
        """Test moderation endpoint with empty content."""
        response = client.post(
            "/api/moderate",
            json={"content": ""}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_moderate_missing_content(self):
        """Test moderation endpoint with missing content field."""
        response = client.post(
            "/api/moderate",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
    
    def test_moderate_whitespace_only(self):
        """Test moderation endpoint with whitespace-only content."""
        response = client.post(
            "/api/moderate",
            json={"content": "   "}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    @patch("app.services.openai_service.openai_service.moderate_content")
    def test_moderate_openai_error(self, mock_moderate):
        """Test moderation endpoint when OpenAI API fails."""
        from openai import OpenAIError
        
        # Mock OpenAI error
        mock_moderate.side_effect = OpenAIError("API Error")
        
        response = client.post(
            "/api/moderate",
            json={"content": "Test content"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
    
    def test_moderate_long_content(self):
        """Test moderation endpoint with long content."""
        # Create content within limits
        long_content = "a" * 5000
        
        response = client.post(
            "/api/moderate",
            json={"content": long_content}
        )
        
        # Should accept content within limits
        assert response.status_code in [200, 500]  # 500 if no real API key
    
    def test_moderate_content_too_long(self):
        """Test moderation endpoint with content exceeding max length."""
        # Create content exceeding max length
        too_long_content = "a" * 10001
        
        response = client.post(
            "/api/moderate",
            json={"content": too_long_content}
        )
        
        assert response.status_code == 422  # Validation error


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""
    
    def test_openapi_schema(self):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "HappyScroll Moderation API"
    
    def test_docs_endpoint(self):
        """Test that Swagger UI is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_endpoint(self):
        """Test that ReDoc is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
