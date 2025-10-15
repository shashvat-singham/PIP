#!/bin/bash

echo "========================================="
echo "Stock Research Chatbot - Startup Script"
echo "========================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please create a .env file with your GEMINI_API_KEY"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)
export PYTHONPATH=$SCRIPT_DIR:$PYTHONPATH

echo "✓ Environment variables loaded"
echo ""

# Start backend
echo "Starting backend server..."
cd "$SCRIPT_DIR"
python3.11 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✓ Backend started (PID: $BACKEND_PID)"
echo "  Logs: /tmp/backend.log"
echo "  URL: http://localhost:8000"
echo ""

# Wait for backend to start
echo "Waiting for backend to be ready..."
for i in {1..10}; do
    if curl -s http://localhost:8000/api/v1/agents > /dev/null 2>&1; then
        echo "✓ Backend is ready!"
        break
    fi
    sleep 1
done
echo ""

# Start frontend
echo "Starting frontend server..."
cd "$SCRIPT_DIR/frontend/stock-research-ui"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install --legacy-peer-deps
fi

# Make vite executable
chmod +x ./node_modules/.bin/vite 2>/dev/null

./node_modules/.bin/vite --host 0.0.0.0 --port 3000 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✓ Frontend started (PID: $FRONTEND_PID)"
echo "  Logs: /tmp/frontend.log"
echo "  URL: http://localhost:3000"
echo ""

echo "========================================="
echo "✓ All services started successfully!"
echo "========================================="
echo ""
echo "Access the application at: http://localhost:3000"
echo ""
echo "To stop all services, run:"
echo "  pkill -f uvicorn && pkill -f vite"
echo ""
echo "To view logs:"
echo "  Backend:  tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""

