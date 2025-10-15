# Stock Research Platform - Architecture Design

## Overview

The Stock Research Platform is an AI-powered application that provides comprehensive stock analysis using **Google Gemini 2.5 Flash**, **LangGraph** for agent orchestration, and real-time data from Yahoo Finance. The system uses a multi-agent architecture with parallel processing capabilities for efficient research.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                  (React + Tailwind CSS)                      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│                    (Python 3.11)                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Yahoo Finance Orchestrator                 │   │
│  │         (Multi-Agent Coordinator)                    │   │
│  └───────────┬──────────────────────────────────────────┘   │
│              │                                               │
│  ┌───────────┴──────────────────────────────────────────┐   │
│  │  Parallel Sub-Agents (ReAct Loops)                   │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • News Agent          • Price Analysis Agent        │   │
│  │  • Earnings Agent      • Technical Analysis Agent    │   │
│  │  • Filings Agent       • Sentiment Agent             │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │                                                │
│  ┌──────────┴───────────────────────────────────────────┐   │
│  │               Data Tools Layer                       │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • Yahoo Finance Tool  (Price, P/E, Metrics)         │   │
│  │  • Web Scraping Tool   (Real-time data)              │   │
│  │  • SEC EDGAR Tool      (Filings, 10-Q, 8-K)          │   │
│  │  • News Aggregator     (Articles with URLs)          │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │                                                │
│  ┌──────────┴───────────────────────────────────────────┐   │
│  │            Gemini AI Service                         │   │
│  │         (Google Gemini 2.5 Flash)                    │   │
│  │  • Analysis Generation  • Summarization              │   │
│  │  • Stance Determination • Confidence Scoring         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Data Sources                      │
├─────────────────────────────────────────────────────────────┤
│  • Yahoo Finance API       • SEC EDGAR Database              │
│  • Web Sources (Live)      • News APIs                       │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend Layer (React)

**Technology**: React 18, Tailwind CSS, Axios

**Responsibilities**:
- User interface for stock analysis requests
- Display of analysis results with citations
- Real-time updates and progress tracking
- Responsive design for desktop and mobile

**Key Features**:
- Ticker input with validation
- Analysis period selection
- Results display with tabs (Summary, Drivers, Risks, Catalysts)
- Citation links with publication dates
- Investment recommendation with confidence level

### 2. Backend API Layer (FastAPI)

**Technology**: FastAPI, Python 3.11, Pydantic

**Responsibilities**:
- RESTful API endpoints
- Request validation and error handling
- CORS configuration
- Health checks and monitoring

**Key Endpoints**:
- `POST /api/analyze` - Analyze stock ticker(s)
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

### 3. Agent Orchestration Layer

**Technology**: LangGraph, Google Gemini 2.5 Flash

**Components**:

#### Yahoo Finance Orchestrator
- Coordinates multiple sub-agents
- Manages parallel execution
- Aggregates results
- Implements ReAct (Reason + Act) loops

#### Sub-Agents
Each agent follows a ReAct loop with strict stop conditions:

1. **News Agent**
   - Fetches recent news articles
   - Extracts URLs and publication dates
   - Summarizes key developments

2. **Price Analysis Agent**
   - Retrieves current and historical prices
   - Calculates technical indicators
   - Identifies support/resistance levels

3. **Financial Metrics Agent**
   - Fetches P/E ratio, EPS, revenue
   - Analyzes profitability margins
   - Compares to industry averages

4. **Technical Analysis Agent**
   - Calculates moving averages (MA 20, MA 50)
   - Determines trend (bullish/bearish/neutral)
   - Identifies price patterns

5. **Sentiment Agent**
   - Analyzes news sentiment
   - Evaluates market perception
   - Tracks insider trading activity

**ReAct Loop Implementation**:
```python
for iteration in range(MAX_ITERATIONS):
    # Think: Analyze current state
    thought = agent.think(context)
    
    # Act: Execute tool/action
    action = agent.act(thought)
    result = execute_action(action)
    
    # Observe: Process results
    observation = agent.observe(result)
    context.update(observation)
    
    # Check stop conditions
    if agent.is_done(context):
        break
```

**Stop Conditions**:
- Task completion (`done` flag)
- Maximum iterations reached (default: 3)
- Timeout exceeded (default: 300s)
- Budget exhausted

### 4. Data Tools Layer

#### Yahoo Finance Tool
**Purpose**: Fetch real-time stock data

**Data Sources**:
- Manus API Hub (YahooFinance/get_stock_chart)
- Direct Yahoo Finance API calls (fallback)
- Web scraping for P/E ratios

**Data Retrieved**:
- Current price
- P/E ratio (TTM)
- 52-week high/low
- Market capitalization
- Company information

#### Web Scraping Tool
**Purpose**: Extract data not available via APIs

**Implementation**:
- BeautifulSoup for HTML parsing
- Regex patterns for data extraction
- Rate limiting and error handling

#### SEC EDGAR Tool
**Purpose**: Retrieve regulatory filings

**Data Retrieved**:
- 10-Q quarterly reports
- 8-K current reports
- Filing dates and URLs

### 5. AI Service Layer

**Technology**: Google Gemini 2.5 Flash

**Capabilities**:
- Natural language understanding
- Context-aware analysis
- Multi-turn conversations
- Structured output generation

**Key Functions**:

1. **News Summarization**
   ```python
   summarize_news(ticker, articles) -> summary
   ```

2. **Investment Analysis**
   ```python
   generate_investment_analysis(
       ticker, 
       stock_info, 
       news_summary, 
       technical_analysis
   ) -> {
       stance: "HOLD" | "BUY" | "SELL",
       confidence: "HIGH" | "MEDIUM" | "LOW",
       rationale: str,
       drivers: List[str],
       risks: List[str],
       catalysts: List[str]
   }
   ```

3. **Technical Analysis**
   ```python
   analyze_support_resistance(ticker, price_data) -> analysis
   ```

## Data Flow

### Request Flow

1. **User Input** → Frontend
   - User enters ticker symbol(s)
   - Selects analysis period
   - Clicks "Analyze"

2. **API Request** → Backend
   - Frontend sends POST request to `/api/analyze`
   - Backend validates request

3. **Orchestration** → Agents
   - Orchestrator spawns parallel sub-agents
   - Each agent executes ReAct loop
   - Results collected and aggregated

4. **Data Fetching** → Tools
   - Yahoo Finance Tool fetches price data
   - Web Scraping Tool extracts P/E ratio
   - News Tool retrieves articles

5. **AI Analysis** → Gemini
   - Gemini analyzes aggregated data
   - Generates investment stance
   - Determines confidence level

6. **Response** → Frontend
   - Backend returns structured JSON
   - Frontend displays results
   - Citations shown with URLs

### Data Structure

**Analysis Response**:
```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "current_price": 247.77,
  "pe_ratio": 37.6,
  "analysis": {
    "stance": "HOLD",
    "confidence": "MEDIUM",
    "rationale": "...",
    "drivers": ["...", "..."],
    "risks": ["...", "..."],
    "catalysts": ["...", "..."]
  },
  "technical_analysis": {
    "trend": "neutral",
    "support_levels": [240.0, 235.0, 230.0],
    "resistance_levels": [250.0, 255.0, 260.0],
    "ma_20": 245.5,
    "ma_50": 243.2
  },
  "news": [
    {
      "title": "...",
      "url": "https://...",
      "published_at": "2025-10-14T10:30:00Z",
      "snippet": "..."
    }
  ],
  "sources": [
    {
      "type": "price_data",
      "url": "https://finance.yahoo.com/quote/AAPL",
      "fetched_at": "2025-10-15T04:46:00Z"
    }
  ]
}
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11
- **AI**: Google Gemini 2.5 Flash
- **Agent Framework**: LangGraph 0.2+
- **Vector DB**: ChromaDB 0.4+
- **Data Fetching**: requests, BeautifulSoup4, yfinance
- **Logging**: structlog
- **Testing**: pytest

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Build Tool**: Create React App

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **API Documentation**: Swagger UI, ReDoc
- **Environment**: .env configuration

## Configuration

### Environment Variables

```bash
# Google Gemini API
GEMINI_API_KEY=your_api_key

# Application
LOG_LEVEL=INFO
ENVIRONMENT=development
MAX_ITERATIONS=3
AGENT_TIMEOUT=300

# CORS
CORS_ORIGINS=http://localhost:3000

# Vector Database
VECTOR_DB_TYPE=chroma
VECTOR_DB_PATH=./data/chroma_db
```

## Security Considerations

1. **API Key Management**
   - Keys stored in `.env` file
   - Never committed to version control
   - Environment-based configuration

2. **Input Validation**
   - Pydantic models for request validation
   - Ticker symbol sanitization
   - Rate limiting on API endpoints

3. **CORS Configuration**
   - Whitelist allowed origins
   - Secure headers
   - HTTPS in production

4. **Data Privacy**
   - No user data storage
   - Temporary session data only
   - No file uploads

## Performance Optimization

1. **Parallel Processing**
   - Sub-agents run in parallel
   - Reduces total analysis time
   - Efficient resource utilization

2. **Caching**
   - Stock data cached for 5 minutes
   - Reduces API calls
   - Improves response time

3. **Timeout Management**
   - Agent timeout: 300s
   - API timeout: 10s
   - Prevents hanging requests

4. **Resource Limits**
   - MAX_ITERATIONS: 3
   - Budget constraints
   - Memory management

## Error Handling

1. **API Errors**
   - Graceful degradation
   - Fallback mechanisms
   - User-friendly error messages

2. **Data Fetching Errors**
   - Retry logic with exponential backoff
   - Alternative data sources
   - Partial results on failure

3. **Agent Errors**
   - Stop condition enforcement
   - Error logging and tracking
   - Recovery mechanisms

## Testing Strategy

1. **Unit Tests**
   - Tool functions
   - Data processing
   - Validation logic

2. **Integration Tests**
   - API endpoints
   - Agent orchestration
   - End-to-end flows

3. **Performance Tests**
   - Latency measurements
   - Throughput testing
   - Resource usage monitoring

## Deployment

### Docker Deployment

```bash
# Build and run
docker-compose up --build

# Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Local Development

```bash
# Backend
cd backend
python scripts/setup.py
uvicorn app.main:app --reload

# Frontend
cd frontend/stock-research-ui
npm install
npm start
```

## Monitoring and Observability

1. **Logging**
   - Structured logging with structlog
   - Per-step timings
   - Error tracking

2. **Health Checks**
   - `/health` endpoint
   - Docker health checks
   - Service monitoring

3. **Metrics**
   - Request latency (p50, p95)
   - Error rates
   - Agent iteration counts

## Future Enhancements

1. **Additional Data Sources**
   - Insider trading data
   - Patent information
   - Academic research papers

2. **Advanced Analysis**
   - Sentiment analysis
   - Comparative analysis
   - Portfolio optimization

3. **UI Improvements**
   - Interactive charts
   - Historical analysis
   - Watchlist management

4. **Performance**
   - Redis caching
   - Database persistence
   - Load balancing

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Yahoo Finance](https://finance.yahoo.com/)
- [SEC EDGAR](https://www.sec.gov/edgar)

