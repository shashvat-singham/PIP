# Stock Research Platform

A professional AI-powered stock research platform that provides comprehensive analysis, real-time market data, and intelligent insights for informed investment decisions.

## 🚀 Quick Start

### Windows

```cmd
# 1. Install dependencies
py scripts/setup.py

# 2. Edit .env and add your GEMINI_API_KEY

# 3. Start the application
py scripts/start.py
```

### Linux/macOS

```bash
# 1. Install dependencies
python3 scripts/setup.py

# 2. Edit .env and add your GEMINI_API_KEY

# 3. Start the application
python3 scripts/start.py
```

### Alternative (Using Convenience Scripts)

**Windows:**
```cmd
setup.bat
REM Edit .env file
start.bat
```

**Linux/macOS:**
```bash
./setup.sh
# Edit .env file
./start.sh
```

## ✨ Features

- **Real-Time Stock Data**: Genuine market data from Yahoo Finance API
- **AI-Powered Analysis**: Multi-agent system using Google Gemini 2.5 Flash
- **Technical Analysis**: Support/resistance levels, moving averages, and trend analysis
- **News Aggregation**: Latest news and market sentiment for any stock
- **Interactive Dashboard**: Modern React-based UI with real-time updates
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Parallel Processing**: Efficient multi-ticker analysis with parallel agents
- **Grounded Insights**: All claims backed by citations with source URLs

## 📋 Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Google Gemini API Key** - [Get API Key](https://ai.google.dev/)

## 📦 Installation

### Step 1: Install Dependencies

**Windows:**
```cmd
cd backend
py scripts\setup.py
```

**Linux/macOS:**
```bash
cd backend
python3 scripts/setup.py
```

This will:
- ✅ Check Python and Node.js versions
- ✅ Install all backend dependencies
- ✅ Install all frontend dependencies
- ✅ Create necessary directories
- ✅ Create `.env` file from template

### Step 2: Configure API Key

Edit the `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### Step 3: Start the Application

**Windows:**
```cmd
cd backend
py scripts\start.py
```

**Linux/macOS:**
```bash
cd backend
python3 scripts/start.py
```

The application will start both backend and frontend servers:
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend UI**: http://localhost:3000

## 🎯 Usage

1. Open http://localhost:3000 in your browser
2. Enter a stock ticker (e.g., AAPL, MSFT, GOOGL)
3. Select analysis period (1 day, 1 week, 1 month, etc.)
4. Click "Analyze"
5. View comprehensive results including:
   - Current price and P/E ratio
   - Technical analysis with support/resistance levels
   - Latest news and sentiment
   - Investment recommendation with confidence level

## 🏛️ Architecture

The application uses a **multi-agent architecture** with specialized agents:

- **Yahoo Finance Orchestrator**: Coordinates data fetching and analysis
- **Stock Data Tool**: Fetches real-time prices and P/E ratios from Yahoo Finance
- **Technical Analysis Agent**: Calculates indicators and identifies trends
- **News Aggregator**: Collects and summarizes market news
- **SEC Edgar Tool**: Retrieves company filings and regulatory documents

For detailed architecture information, see [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md).

## 🚀 Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **AI/ML**: Google Gemini 2.5 Flash
- **Agent Framework**: LangGraph
- **Vector DB**: ChromaDB
- **Data Sources**: Yahoo Finance API, Web Scraping, SEC EDGAR
- **Logging**: Structlog
- **Testing**: Pytest

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **HTTP Client**: Axios

## 🐳 Docker Deployment

```bash
# 1. Configure .env file
cp .env.template .env
# Edit .env and add your GEMINI_API_KEY

# 2. Build and run
docker-compose up --build
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📖 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "analysis_type": "comprehensive",
    "time_period": "1mo"
  }'
```

## 🧪 Testing

```bash
cd backend
pytest
```

Run with coverage:
```bash
pytest --cov=backend --cov-report=html
```

## ✅ Data Accuracy

All stock data is **genuine and real-time**, sourced directly from Yahoo Finance:

- ✅ Current prices match Yahoo Finance exactly
- ✅ P/E ratios scraped from official source
- ✅ No dummy or fallback data
- ✅ Real-time updates
- ✅ Works for any valid ticker symbol

## 📁 Project Structure

```
stock-research-platform/
├── backend/
│   ├── agents/              # AI agents for analysis
│   ├── app/                 # FastAPI application
│   ├── tools/               # Data fetching tools
│   ├── utils/               # Utility modules
│   ├── services/            # Gemini AI service
│   ├── tests/               # Test suite
│   ├── scripts/             # Setup and start scripts
│   │   ├── setup.py         # Dependency installation
│   │   └── start.py         # Application startup
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── stock-research-ui/   # React application
├── setup.bat                # Windows setup script
├── start.bat                # Windows start script
├── setup.sh                 # Linux/macOS setup script
├── start.sh                 # Linux/macOS start script
├── .env.template            # Environment template
├── docker-compose.yml       # Docker configuration
├── README.md                # This file
├── ARCHITECTURE_DESIGN.md   # Architecture details
└── SETUP_GUIDE.md           # Detailed setup guide
```

## 🔧 Command Line Options

### Setup Script

```bash
# Force reinstall all dependencies
python scripts/setup.py --force

# Install only backend dependencies
python scripts/setup.py --backend-only

# Install only frontend dependencies
python scripts/setup.py --frontend-only
```

### Start Script

```bash
# Start only backend
python scripts/start.py --backend-only

# Start only frontend
python scripts/start.py --frontend-only

# Use custom ports
python scripts/start.py --backend-port 8001 --frontend-port 3001
```

## 🔒 Security

- ✅ API keys stored in `.env` (not in code)
- ✅ `.gitignore` configured to exclude sensitive files
- ✅ CORS properly configured
- ✅ Input validation on all endpoints
- ✅ No file uploads allowed
- ✅ Rate limiting implemented

## 📞 Support

For issues and questions:
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions
- Review [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) for technical details
- Check logs in `logs/` directory
- Visit API docs at http://localhost:8000/docs

## 🙏 Acknowledgments

- **Yahoo Finance** for market data
- **Google Gemini** for AI capabilities
- **FastAPI** and **React** communities
- **SEC EDGAR** for regulatory filings

## 📄 License

This project is licensed under the MIT License.

---

**🚀 Ready to analyze stocks with AI!**

