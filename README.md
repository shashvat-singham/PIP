# Stock Research Agentic Chatbot

This project is an AI-powered, multi-agent chatbot designed for comprehensive stock research and analysis. It takes natural language queries about multiple stock tickers, spawns parallel research agents to gather information from various sources, and synthesizes the findings into actionable insights and investment recommendations.

## ✨ Features

- **Multi-Agent Architecture**: Utilizes a team of specialized agents (News, Filings, Earnings, etc.) for in-depth research.
- **Parallel Processing**: Spawns parallel research agents per ticker for efficient and fast analysis.
- **Real-time Web Research**: Gathers up-to-the-minute information from web sources, financial data APIs, and SEC filings.
- **Grounded Insights**: All claims and insights are backed by citations with source URLs and publication dates.
- **Investment Recommendations**: Provides a clear investment stance (Buy, Hold, Sell) with a confidence level and detailed rationale.
- **Dual Frontend Options**: Comes with both a modern React-based UI and a functional Streamlit UI.
- **Containerized Deployment**: Packaged with Docker for easy, one-command setup and deployment.
- **Comprehensive Testing**: Includes a full suite of unit and integration tests to ensure reliability.

## 🏛️ System Architecture

The application is built with a modern, scalable architecture:

- **Backend**: FastAPI (Python) provides a robust API for handling analysis requests.
- **Agent Framework**: LangGraph is used to orchestrate the complex, multi-agent workflows.
- **Language Model**: Google's Gemini 2.5 Flash powers the natural language understanding and generation.
- **Frontend**: 
    - **React**: A rich, interactive user interface built with React, Tailwind CSS, and shadcn/ui.
    - **Streamlit**: A simple, data-centric user interface for quick analysis and prototyping.
- **Data Sources**: Integrates with real-time financial data APIs and SEC EDGAR for comprehensive data gathering.
- **Containerization**: Docker and Docker Compose are used for packaging and running the application.

For a more detailed overview of the architecture, please see the [Architecture Document](docs/ARCHITECTURE.md).

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js and npm (for React frontend development)
- A Gemini API key
- (Optional) Docker and Docker Compose for containerized deployment

### Quickstart with Docker (Optional)

If you prefer to run the application using Docker, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd stock-research-chatbot
    ```

2.  **Set up your environment:**
    - Copy the `.env.template` file to `.env`:
      ```bash
      cp .env.template .env
      ```
    - Edit the `.env` file and add your Gemini API key:
      ```
      GEMINI_API_KEY=your_gemini_api_key_here
      ```

3.  **Build and run with Docker Compose:**
    ```bash
    ./scripts/deploy.sh
    ```

4.  **Access the application:**
    - **Backend API**: `http://localhost:8000`
    - **API Docs**: `http://localhost:8000/docs`
    - **Streamlit UI**: `http://localhost:8501`
    - **React UI**: The React UI is not started by default with `deploy.sh`. To run it, see the development setup below.

### Development Setup (Recommended for VSCode Terminal)

For more detailed instructions on setting up a local development environment, please see the [Getting Started Guide](docs/GETTING_STARTED.md).

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd stock-research-chatbot
    ```

2.  **Run the setup script:**
    This script will check prerequisites, create a Python virtual environment, install dependencies, and create necessary directories.
    ```bash
    python scripts/setup.py
    ```

3.  **Activate the virtual environment:**
    - On Linux/macOS:
      ```bash
      source venv/bin/activate
      ```
    - On Windows (Command Prompt):
      ```cmd
      .\venv\Scripts\activate.bat
      ```
    - On Windows (PowerShell):
      ```powershell
      .\venv\Scripts\Activate.ps1
      ```

4.  **Set up your environment variables:**
    - Copy the `.env.template` file to `.env` if `setup.py` didn't create it:
      ```bash
      cp .env.template .env
      ```
    - Edit the `.env` file and add your Gemini API key:
      ```
      GEMINI_API_KEY=your_gemini_api_key_here
      ```

5.  **Start the application:**
    - To start the backend and React frontend:
      ```bash
      python scripts/start.py --frontend react
      ```
    - To start the backend and Streamlit frontend:
      ```bash
      python scripts/start.py --frontend streamlit
      ```
    - To start both frontends:
      ```bash
      python scripts/start.py --frontend both
      ```
    - To install dependencies during startup (if not already done by `setup.py` or if you want to force reinstall):
      ```bash
      python scripts/start.py --frontend react --install-deps
      ```

## 📖 Usage

1.  **Open the web interface** (React or Streamlit).
2.  **Enter a query** in the text area. Your query should include one or more stock tickers and a description of what you want to analyze.
    - *Example*: `Analyze NVDA, AMD, and TSM for their exposure to AI datacenter demand. What is the short-term outlook (3-6 months)?`
3.  **Click the "Analyze" button** to start the research process.
4.  **View the results**: The application will display a detailed breakdown of the analysis for each ticker, including a summary, key drivers, risks, catalysts, and the final investment recommendation.

## 🧪 Testing

The project includes a comprehensive test suite to ensure code quality and reliability. To run the tests:

1.  Make sure you have set up the development environment and installed all dependencies.
2.  Activate your virtual environment.
3.  Run the tests using pytest:
    ```bash
    pytest
    ```

## 🔒 Security

Please review the [Security Policy](SECURITY.md) for information on security-related matters.

## 📜 Changelog

For a detailed list of changes, please see the [Changelog](CHANGELOG.md).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

