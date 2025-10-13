"""
Test suite for the Stock Research Chatbot API.
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models import AnalysisRequest, TickerInsight, StanceType, ConfidenceLevel
from backend.agents.orchestrator import ResearchOrchestrator


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
        assert len(data["agents"]) == 6  # We have 6 agent types
        
        # Check that all expected agent types are present
        agent_types = [agent["type"] for agent in data["agents"]]
        expected_types = ["news", "filings", "earnings", "insider", "patents", "price"]
        
        for expected_type in expected_types:
            assert expected_type in agent_types
    
    @patch('backend.agents.orchestrator.ResearchOrchestrator.analyze')
    def test_analyze_stocks_success(self, mock_analyze):
        """Test successful stock analysis."""
        # Mock the analysis result
        mock_insight = TickerInsight(
            ticker="AAPL",
            company_name="Apple Inc.",
            summary="Strong financial performance with solid growth prospects.",
            key_drivers=["iPhone sales growth", "Services revenue expansion"],
            risks=["Supply chain disruptions", "Regulatory challenges"],
            catalysts=["New product launches", "Market expansion"],
            stance=StanceType.BUY,
            confidence=ConfidenceLevel.HIGH,
            rationale="Strong fundamentals and positive outlook justify buy recommendation.",
            sources=[],
            agent_traces=[]
        )
        
        mock_analyze.return_value = [mock_insight]
        
        # Make the API request
        request_data = {
            "query": "Analyze AAPL for investment potential",
            "max_iterations": 3,
            "timeout_seconds": 30
        }
        
        response = self.client.post("/api/v1/analyze", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert len(data["insights"]) == 1
        assert data["insights"][0]["ticker"] == "AAPL"
        assert data["insights"][0]["stance"] == "buy"
        assert data["insights"][0]["confidence"] == "high"
        assert "request_id" in data
        assert "total_latency_ms" in data
    
    def test_analyze_stocks_invalid_request(self):
        """Test analysis with invalid request data."""
        # Empty query
        response = self.client.post("/api/v1/analyze", json={"query": ""})
        assert response.status_code == 422  # Validation error
        
        # Missing query
        response = self.client.post("/api/v1/analyze", json={})
        assert response.status_code == 422  # Validation error
    
    @patch('backend.agents.orchestrator.ResearchOrchestrator.analyze')
    def test_analyze_stocks_failure(self, mock_analyze):
        """Test analysis failure handling."""
        # Mock an exception
        mock_analyze.side_effect = Exception("Analysis failed")
        
        request_data = {
            "query": "Analyze INVALID for investment potential",
            "max_iterations": 3,
            "timeout_seconds": 30
        }
        
        response = self.client.post("/api/v1/analyze", json=request_data)
        assert response.status_code == 500
        
        data = response.json()
        assert "Analysis failed" in data["detail"]
    
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


class TestOrchestrator:
    """Test cases for the Research Orchestrator."""
    
    def setup_method(self):
        """Set up test orchestrator."""
        self.orchestrator = ResearchOrchestrator()
    
    def test_extract_tickers(self):
        """Test ticker extraction from queries."""
        # Test basic ticker extraction
        query1 = "Analyze AAPL and MSFT for growth potential"
        tickers1 = self.orchestrator._extract_tickers(query1)
        assert "AAPL" in tickers1
        assert "MSFT" in tickers1
        
        # Test with more complex query
        query2 = "Compare NVDA, AMD, and TSM for AI datacenter demand"
        tickers2 = self.orchestrator._extract_tickers(query2)
        assert "NVDA" in tickers2
        assert "AMD" in tickers2
        assert "TSM" in tickers2
        
        # Test with no tickers
        query3 = "What is the market outlook?"
        tickers3 = self.orchestrator._extract_tickers(query3)
        assert len(tickers3) == 0
        
        # Test filtering common words
        query4 = "Analyze THE BEST stocks FOR investment"
        tickers4 = self.orchestrator._extract_tickers(query4)
        # Should not include common words like THE, BEST, FOR
        common_words = {"THE", "BEST", "FOR"}
        for word in common_words:
            assert word not in tickers4
    
    @pytest.mark.asyncio
    async def test_analyze_timeout(self):
        """Test analysis timeout handling."""
        query = "Analyze AAPL"
        
        # Test with very short timeout
        with pytest.raises(Exception) as exc_info:
            await self.orchestrator.analyze(
                query=query,
                max_iterations=3,
                timeout_seconds=0.001,  # Very short timeout
                request_id="test-timeout"
            )
        
        assert "timed out" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_analyze_no_tickers(self):
        """Test analysis with no valid tickers."""
        query = "What is the general market outlook?"
        
        with pytest.raises(Exception) as exc_info:
            await self.orchestrator.analyze(
                query=query,
                max_iterations=3,
                timeout_seconds=30,
                request_id="test-no-tickers"
            )
        
        assert "no valid stock tickers" in str(exc_info.value).lower()


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
