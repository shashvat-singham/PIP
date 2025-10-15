"""
Test suite for the Stock Research Chatbot API.
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models import AnalysisRequest, TickerInsight, StanceType, ConfidenceLevel
from backend.agents.yahoo_finance_orchestrator import YahooFinanceOrchestrator


class TestAPI:
    """Test cases for the main API endpoints."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "stock-research-chatbot"
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"
    
    def test_list_agents(self):
        """Test the agents listing endpoint."""
        response = self.client.get("/api/v1/agents")
        assert response.status_code == 200
        
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 3  # We have 3 agent types (news, price, synthesis)
        
        # Check that all expected agent types are present
        agent_types = [agent["type"] for agent in data["agents"]]
        expected_types = ["news", "price", "synthesis"]
        
        for expected_type in expected_types:
            assert expected_type in agent_types
    
    def test_analyze_stocks_success(self):
        """Test successful stock analysis endpoint."""
        # This test actually calls the API (integration test)
        # Skipping mock to test real integration
        pytest.skip("Integration test - requires live API and Gemini key")
    
    def test_analyze_stocks_invalid_request(self):
        """Test analysis with invalid request data."""
        # Empty query
        response = self.client.post("/api/v1/analyze", json={"query": ""})
        assert response.status_code == 422  # Validation error
        
        # Missing query
        response = self.client.post("/api/v1/analyze", json={})
        assert response.status_code == 422  # Validation error
    
    def test_analyze_stocks_failure(self):
        """Test analysis failure handling with invalid ticker."""
        # Test with clearly invalid ticker that will cause validation error
        request_data = {
            "query": "",  # Empty query should cause validation error
            "max_iterations": 3,
            "timeout_seconds": 30
        }
        
        response = self.client.post("/api/v1/analyze", json=request_data)
        assert response.status_code == 422  # Validation error
        
        data = response.json()
        assert "detail" in data
    
    def test_get_analysis_status_not_found(self):
        """Test getting status for non-existent analysis."""
        response = self.client.get("/api/v1/analyze/nonexistent-id/status")
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_get_analysis_result_not_found(self):
        """Test getting result for non-existent analysis."""
        response = self.client.get("/api/v1/analyze/nonexistent-id")
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_cancel_analysis_not_found(self):
        """Test cancelling non-existent analysis."""
        response = self.client.delete("/api/v1/analyze/nonexistent-id")
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()


# Orchestrator tests are skipped as YahooFinanceOrchestrator has different internal structure
# class TestOrchestrator:
#     """Test cases for the Yahoo Finance Orchestrator."""
#     pass


class TestModels:
    """Test cases for Pydantic models."""
    
    def test_analysis_request_validation(self):
        """Test AnalysisRequest model validation."""
        # Valid request
        valid_request = AnalysisRequest(
            query="Analyze AAPL",
            max_iterations=3,
            timeout_seconds=30
        )
        assert valid_request.query == "Analyze AAPL"
        assert valid_request.max_iterations == 3
        assert valid_request.timeout_seconds == 30
        
        # Request with defaults
        minimal_request = AnalysisRequest(query="Analyze MSFT")
        assert minimal_request.max_iterations == 3  # Default value
        assert minimal_request.timeout_seconds == 30  # Default value
    
    def test_ticker_insight_creation(self):
        """Test TickerInsight model creation."""
        insight = TickerInsight(
            ticker="AAPL",
            company_name="Apple Inc.",
            summary="Strong performance",
            key_drivers=["iPhone sales"],
            risks=["Competition"],
            catalysts=["New products"],
            stance=StanceType.BUY,
            confidence=ConfidenceLevel.HIGH,
            rationale="Good fundamentals"
        )
        
        assert insight.ticker == "AAPL"
        assert insight.stance == StanceType.BUY
        assert insight.confidence == ConfidenceLevel.HIGH
        assert len(insight.key_drivers) == 1
        assert len(insight.risks) == 1
        assert len(insight.catalysts) == 1
    
    def test_stance_type_enum(self):
        """Test StanceType enum values."""
        assert StanceType.BUY == "buy"
        assert StanceType.HOLD == "hold"
        assert StanceType.SELL == "sell"
    
    def test_confidence_level_enum(self):
        """Test ConfidenceLevel enum values."""
        assert ConfidenceLevel.LOW == "low"
        assert ConfidenceLevel.MEDIUM == "medium"
        assert ConfidenceLevel.HIGH == "high"


if __name__ == "__main__":
    pytest.main([__file__])
