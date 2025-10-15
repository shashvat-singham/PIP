# Stock Research Platform - Quick Start Guide

## ⚡ Get Started in 3 Steps

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

### Step 2: Configure API Key

Edit `.env` file and add your Gemini API key:
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

## 🎯 Access Points

Once started, access:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔑 API Key

Your working Gemini API key:
```
GEMINI_API_KEY=AIzaSyCftQ4AkSSmEf1Uk_QkmzoRo82zKhGd6lQ
```

## 📝 Example Usage

1. Open http://localhost:3000
2. Enter ticker: `AAPL`
3. Select period: `1 Month`
4. Click "Analyze"
5. View results with real-time data!

## 🛠️ Troubleshooting

### Import Error
If you see `ModuleNotFoundError: No module named 'data_api'`:
```bash
cd backend
python scripts/setup.py --force
```

### Port Already in Use
Use custom ports:
```bash
python scripts/start.py --backend-port 8001 --frontend-port 3001
```

### Dependencies Not Installed
Reinstall:
```bash
python scripts/setup.py --force
```

## 📚 More Information

- **Full Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Architecture**: [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md)
- **Main README**: [README.md](README.md)

---

**That's it! You're ready to go! 🚀**

