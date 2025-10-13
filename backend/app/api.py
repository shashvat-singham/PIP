"""
API routes for the Stock Research Chatbot.
"""
import uuid
import time
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import structlog

from backend.app.models import (
    AnalysisRequest, 
    AnalysisResponse, 
    AnalysisStatus,
    TickerInsight,
    StanceType,
    ConfidenceLevel
)
from backend.agents.simple_orchestrator import SimpleResearchOrchestrator
from backend.config.settings import get_settings

logger = structlog.get_logger()
router = APIRouter()

# In-memory storage for analysis status (in production, use Redis or similar)
analysis_status_store: Dict[str, Dict[str, Any]] = {}


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_stocks(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze stocks based on natural language query.
    
    This endpoint triggers the multi-agent research process for the specified stocks.
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()
    started_at = datetime.now()
    
    logger.info("Starting stock analysis", 
                request_id=request_id, 
                query=request.query)
    
    try:
        # Initialize the research orchestrator
        orchestrator = SimpleResearchOrchestrator()
        
        # Update status
        analysis_status_store[request_id] = {
            "status": "processing",
            "progress": 0.0,
            "current_step": "Initializing analysis",
            "started_at": started_at
        }
        
        # Run the analysis
        insights = await orchestrator.analyze(
            query=request.query,
            max_iterations=request.max_iterations or 3,
            timeout_seconds=request.timeout_seconds or 30,
            request_id=request_id
        )
        
        # Calculate execution time
        end_time = time.time()
        total_latency_ms = (end_time - start_time) * 1000
        
        # Extract tickers and agents used
        tickers_analyzed = [insight.ticker for insight in insights]
        agents_used = list(set([
            trace.agent_type 
            for insight in insights 
            for trace in insight.agent_traces
        ]))
        
        # Create response
        response = AnalysisResponse(
            request_id=request_id,
            query=request.query,
            insights=insights,
            total_latency_ms=total_latency_ms,
            tickers_analyzed=tickers_analyzed,
            agents_used=agents_used,
            started_at=started_at,
            completed_at=datetime.now()
        )
        
        # Update final status
        analysis_status_store[request_id] = {
            "status": "completed",
            "progress": 100.0,
            "current_step": "Analysis complete",
            "completed_at": datetime.now()
        }
        
        logger.info("Stock analysis completed", 
                    request_id=request_id,
                    tickers_count=len(tickers_analyzed),
                    latency_ms=total_latency_ms)
        
        return response
        
    except Exception as e:
        logger.error("Stock analysis failed", 
                     request_id=request_id, 
                     error=str(e))
        
        # Update error status
        analysis_status_store[request_id] = {
            "status": "failed",
            "progress": 0.0,
            "current_step": f"Error: {str(e)}",
            "error": str(e)
        }
        
        if "No valid stock tickers found in query" in str(e):
            raise HTTPException(
                status_code=422,
                detail=f"Validation Error: {str(e)}"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )



@router.get("/analyze/{request_id}/status", response_model=AnalysisStatus)
async def get_analysis_status(request_id: str) -> AnalysisStatus:
    """Get the status of an ongoing analysis."""
    if request_id not in analysis_status_store:
        raise HTTPException(
            status_code=404,
            detail="Analysis request not found"
        )
    
    status_data = analysis_status_store[request_id]
    
    return AnalysisStatus(
        request_id=request_id,
        status=status_data["status"],
        progress=status_data["progress"],
        current_step=status_data.get("current_step"),
        estimated_completion=status_data.get("estimated_completion")
    )


@router.get("/analyze/{request_id}")
async def get_analysis_result(request_id: str) -> Dict[str, Any]:
    """Get the result of a completed analysis."""
    if request_id not in analysis_status_store:
        raise HTTPException(
            status_code=404,
            detail="Analysis request not found"
        )
    
    status_data = analysis_status_store[request_id]
    
    if status_data["status"] != "completed":
        return {
            "request_id": request_id,
            "status": status_data["status"],
            "message": "Analysis not yet completed"
        }
    
    # In a real implementation, you'd retrieve the full result from storage
    return {
        "request_id": request_id,
        "status": "completed",
        "message": "Analysis completed successfully"
    }


@router.delete("/analyze/{request_id}")
async def cancel_analysis(request_id: str) -> Dict[str, str]:
    """Cancel an ongoing analysis."""
    if request_id not in analysis_status_store:
        raise HTTPException(
            status_code=404,
            detail="Analysis request not found"
        )
    
    # Update status to cancelled
    analysis_status_store[request_id]["status"] = "cancelled"
    analysis_status_store[request_id]["current_step"] = "Analysis cancelled by user"
    
    logger.info("Analysis cancelled", request_id=request_id)
    
    return {
        "request_id": request_id,
        "message": "Analysis cancelled successfully"
    }


@router.get("/agents")
async def list_available_agents() -> Dict[str, Any]:
    """List all available research agents and their capabilities."""
    return {
        "agents": [
            {
                "type": "news",
                "description": "Searches for recent news articles and press releases",
                "capabilities": ["web_search", "news_aggregation", "sentiment_analysis"]
            },
            {
                "type": "filings",
                "description": "Analyzes SEC filings and regulatory documents",
                "capabilities": ["sec_edgar_access", "document_parsing", "financial_analysis"]
            },
            {
                "type": "earnings",
                "description": "Reviews earnings calls and transcripts",
                "capabilities": ["transcript_analysis", "earnings_data", "guidance_extraction"]
            },
            {
                "type": "insider",
                "description": "Tracks insider trading and ownership changes",
                "capabilities": ["insider_trading_data", "ownership_analysis", "institutional_holdings"]
            },
            {
                "type": "patents",
                "description": "Researches patents and academic papers",
                "capabilities": ["patent_search", "academic_research", "innovation_tracking"]
            },
            {
                "type": "price",
                "description": "Analyzes price movements and technical factors",
                "capabilities": ["price_analysis", "technical_indicators", "market_sentiment"]
            }
        ]
    }
