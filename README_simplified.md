# Stock Research Agentic Chatbot - Simplified Quick Start

This guide provides a simplified set of instructions to get the Stock Research Chatbot application running.

### 🖥 Backend Setup

```bash
cd stock-research-chatbot
pip install -r backend/requirements.txt
py -m backend.app.main
```

### 💻 Frontend Setup

```bash
cd frontend/stock-research-ui
npm install --legacy-peer-deps
npm run dev
```

### 🌐 Access the App

Open your browser and go to:
http://localhost:5173

## 🧪 Test Backend API with Postman

### 1️⃣ Open Postman and create a new request
- Method: **POST**
- URL:  
  ```
  http://127.0.0.1:8000/api/v1/analyze
  ```

### 2️⃣ Go to the **Body** tab
- Select **raw**
- From the dropdown on the right, select **JSON**
- Paste the following JSON payload:
  ```json
  {
    "query": "Analyze AAPL stock for 1 month",
    "max_iterations": 3,
    "timeout_seconds": 60
  }
  ```

### 3️⃣ Go to the **Headers** tab
Add this header:
| Key | Value |
|-----|--------|
| Content-Type | application/json |

### 4️⃣ Click **Send**
You should receive a **200 OK** response with the AI-generated stock analysis.

---