# Crisis Management AI System 🚨

## 🎯 Overview
AI-powered emergency response system for natural disasters using **Google Gemini AI**. Intelligently processes distress messages, prioritizes them with time-aware scoring, and provides a real-time dashboard for emergency responders.

## ✨ Key Features
- 🤖 **AI-Powered Analysis** - Gemini AI interprets unstructured emergency messages
- ⏰ **Time-Aware Prioritization** - Nighttime shelter = higher priority
- 📍 **Location-Based Filtering** - Filter by geographic areas
- 👥 **Vulnerable Population Detection** - Automatically identifies children, elderly, pregnant
- 📊 **Real-Time Dashboard** - Web interface for emergency responders
- 🔄 **Auto-Refresh** - Updates every 30 seconds

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Gemini API Key
Get your free API key at: https://makersuite.google.com/app/apikey

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Process Test Messages
```bash
python process_messages.py
```

### 4. Launch Dashboard
```bash
python app.py
```

### 5. Open Dashboard
Navigate to: **http://localhost:5000**

## 📂 Project Structure
```
crisis_resource_matching/
├── ai_processor.py          # Gemini AI integration
├── priority_engine.py       # Time-aware scoring
├── database.py              # JSON storage
├── app.py                   # Flask web app
├── process_messages.py      # Demo script
├── config.py                # Configuration
├── requirements.txt         # Dependencies
├── templates/               # HTML templates
├── static/                  # CSS & JavaScript
└── data/                    # Messages & database
```

## 👥 Team Division (for Hackathon)

**PERSON 1: AI Backend**
- `ai_processor.py`
- `priority_engine.py`
- `database.py`

**PERSON 2: Frontend**
- `app.py`
- `templates/dashboard.html`
- `static/style.css`
- `static/script.js`

**📘 See [HACKATHON_README.md](HACKATHON_README.md) for detailed 6-hour timeline and step-by-step instructions!**

## 📊 Tech Stack
- Google Gemini AI
- Flask (Web Framework)
- Python 3.8+
- Vanilla JavaScript

## 📝 Note
The original rule-based system is preserved in `main.py` for reference. The new AI system uses Gemini for intelligent message interpretation.

---

**For hackathon participants:** Check [HACKATHON_README.md](HACKATHON_README.md) for complete setup guide!
