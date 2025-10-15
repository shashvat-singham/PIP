# Stock Research Platform - Setup Guide

This guide will help you set up and run the Stock Research Platform on your local machine (Windows, macOS, or Linux).

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Optional
- **Docker Desktop** - [Download Docker](https://www.docker.com/products/docker-desktop) (for containerized deployment)

### API Keys
- **Google Gemini API Key** - [Get API Key](https://ai.google.dev/)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd stock-research-platform
```

### 2. Run the Setup Script

The setup script will automatically:
- Check Python and Node.js versions
- Install backend dependencies
- Install frontend dependencies
- Create necessary directories
- Create `.env` file from template

#### On Windows (Command Prompt):
```cmd
cd backend
python scripts\setup.py
```

#### On Windows (PowerShell):
```powershell
cd backend
python scripts/setup.py
```

#### On macOS/Linux:
```bash
cd backend
python3 scripts/setup.py
```

### 3. Configure Environment Variables

Edit the `.env` file in the root directory and add your Gemini API key:

```bash
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Example `.env` file:**
```env
# Google Gemini API Configuration
GEMINI_API_KEY=AIzaSyCftQ4AkSSmEf1Uk_QkmzoRo82zKhGd6lQ

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development

# CORS Configuration
CORS_ORIGINS=http://localhost:3000
```

## Running the Application

### Option 1: Run Locally (Recommended for Development)

#### Start the Backend Server

Open a terminal and run:

**Windows:**
```cmd
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**macOS/Linux:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Start the Frontend Server

Open a **new terminal** and run:

```bash
cd frontend/stock-research-ui
npm start
```

The frontend will be available at:
- **UI**: http://localhost:3000

### Option 2: Run with Docker

If you have Docker installed, you can run the entire application with one command:

```bash
docker-compose up --build
```

This will start both the backend and frontend services.

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

To stop the services:
```bash
docker-compose down
```

## Verifying the Installation

### 1. Check Backend Health

Open your browser and navigate to:
```
http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Check API Documentation

Navigate to:
```
http://localhost:8000/docs
```

You should see the Swagger UI with all available API endpoints.

### 3. Test the Frontend

Navigate to:
```
http://localhost:3000
```

You should see the Stock Research Platform interface.

### 4. Run a Test Analysis

1. Enter a stock ticker (e.g., `AAPL`)
2. Select an analysis period (e.g., `1 Month`)
3. Click "Analyze"
4. Wait for the results

You should see:
- Current price
- P/E ratio
- Technical analysis
- News articles
- Investment recommendation

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

To run tests with coverage:
```bash
pytest --cov=backend --cov-report=html
```

### Frontend Tests

```bash
cd frontend/stock-research-ui
npm test
```

## Troubleshooting

### Common Issues

#### 1. `ModuleNotFoundError: No module named 'data_api'`

**Solution**: The application now uses a wrapper module that works both locally and in Manus environment. Make sure you've run the setup script and installed all dependencies.

```bash
cd backend
pip install -r requirements.txt
```

#### 2. `GEMINI_API_KEY not found`

**Solution**: Make sure you've created the `.env` file and added your API key.

```bash
# Check if .env exists
ls -la .env

# If not, copy from template
cp .env.template .env

# Edit and add your API key
nano .env  # or use any text editor
```

#### 3. Port Already in Use

**Solution**: If port 8000 or 3000 is already in use, you can change the ports:

**Backend** (change port in command):
```bash
uvicorn app.main:app --reload --port 8001
```

**Frontend** (create `.env` file in `frontend/stock-research-ui`):
```env
PORT=3001
```

#### 4. `npm install` Fails

**Solution**: Clear npm cache and try again:

```bash
cd frontend/stock-research-ui
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 5. Python Version Mismatch

**Solution**: Make sure you're using Python 3.11+:

```bash
python --version  # or python3 --version
```

If you have multiple Python versions, use the specific version:
```bash
python3.11 -m pip install -r requirements.txt
python3.11 -m uvicorn app.main:app --reload
```

#### 6. CORS Errors in Browser

**Solution**: Make sure the backend is running and CORS is configured correctly in `.env`:

```env
CORS_ORIGINS=http://localhost:3000
```

### Windows-Specific Issues

#### PowerShell Execution Policy

If you get an error about execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Path Issues

Use backslashes for paths in Windows:
```cmd
cd backend\scripts
python setup.py
```

### macOS/Linux-Specific Issues

#### Permission Denied

Make scripts executable:
```bash
chmod +x backend/scripts/setup.py
```

## Development Workflow

### 1. Making Changes to Backend

1. Edit Python files in `backend/`
2. The server will automatically reload (if using `--reload` flag)
3. Test your changes at http://localhost:8000/docs

### 2. Making Changes to Frontend

1. Edit React files in `frontend/stock-research-ui/src/`
2. The browser will automatically refresh
3. View changes at http://localhost:3000

### 3. Running Tests Before Committing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend/stock-research-ui
npm test
```

## Project Structure

```
stock-research-platform/
├── backend/
│   ├── agents/              # AI agents
│   ├── app/                 # FastAPI application
│   ├── tools/               # Data fetching tools
│   ├── utils/               # Utilities
│   ├── services/            # Gemini AI service
│   ├── tests/               # Test suite
│   ├── scripts/             # Setup scripts
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── stock-research-ui/
│       ├── src/             # React source code
│       ├── public/          # Static files
│       └── package.json     # Node dependencies
├── data/                    # Data storage
├── logs/                    # Application logs
├── .env                     # Environment variables
├── .env.template            # Environment template
├── docker-compose.yml       # Docker configuration
├── README.md                # Main documentation
├── ARCHITECTURE_DESIGN.md   # Architecture details
├── SETUP_GUIDE.md           # This file
└── FIX_SUMMARY.md           # Recent fixes
```

## Next Steps

1. ✅ **Verify Installation** - Run health checks
2. ✅ **Test with Sample Data** - Analyze AAPL or MSFT
3. ✅ **Read Documentation** - Check ARCHITECTURE_DESIGN.md
4. ✅ **Explore API** - Visit http://localhost:8000/docs
5. ✅ **Customize** - Modify agents or add new features

## Getting Help

- **Documentation**: Check README.md and ARCHITECTURE_DESIGN.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: Create an issue on GitHub
- **Logs**: Check `logs/` directory for error messages

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Google Gemini API](https://ai.google.dev/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Yahoo Finance](https://finance.yahoo.com/)

---

**Happy Analyzing! 📈**

