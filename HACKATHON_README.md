# 🚨 Crisis Management AI System - Hackathon Project

## 🎯 Project Overview

An AI-powered emergency response system that intelligently processes and prioritizes distress messages during natural disasters using Google Gemini AI. Built for **emergency responders** to efficiently manage crisis situations with location-based filtering and time-aware prioritization.

---

## ✨ Key Features

✅ **AI-Powered Message Analysis** - Gemini AI interprets unstructured emergency messages  
✅ **Smart Prioritization** - Time-aware scoring (e.g., nighttime shelter = higher priority)  
✅ **Location-Based Filtering** - Filter by geographic areas  
✅ **Real-Time Dashboard** - Web interface for emergency responders  
✅ **Vulnerable Population Detection** - Identifies children, elderly, pregnant individuals  
✅ **Multi-Factor Scoring** - Base urgency + time sensitivity + vulnerable groups + danger level  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│           SMS / Social Media Messages           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│         AI Processor (Gemini AI)                │
│  - Extracts: need, location, urgency            │
│  - Detects: vulnerable groups, danger level     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│         Priority Engine                          │
│  - Time-aware scoring                           │
│  - Multi-factor weighting                       │
│  - CRITICAL/HIGH/MEDIUM/LOW classification      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│         Web Dashboard                            │
│  - Location filtering                           │
│  - Real-time updates                            │
│  - Status management                            │
└─────────────────────────────────────────────────┘
```

---

## 👥 Team Division (2 People, 6 Hours)

### 🔵 **PERSON 1: AI Backend Developer** (3-4 hours)

**Files to work on:**
- `ai_processor.py` - Gemini AI integration
- `priority_engine.py` - Scoring logic
- `database.py` - Data storage
- `config.py` - Settings
- `process_messages.py` - Testing/demo

**Tasks:**
1. **Hour 1**: Get Gemini API key, set up environment, test AI processor
2. **Hour 2**: Fine-tune priority engine weights and time-sensitive scoring
3. **Hour 3**: Test with real messages, adjust fallback logic
4. **Hour 4**: Integration testing with Person 2

**Key Responsibilities:**
- Ensure AI accurately extracts need, location, urgency
- Optimize time-based prioritization (nighttime shelter boost)
- Handle API errors gracefully with fallback
- Test edge cases (missing location, unclear needs)

---

### 🟢 **PERSON 2: Frontend Developer** (3-4 hours)

**Files to work on:**
- `app.py` - Flask backend API
- `templates/dashboard.html` - UI structure
- `static/style.css` - Styling
- `static/script.js` - Interactive features

**Tasks:**
1. **Hour 1**: Set up Flask, test basic routes, ensure UI loads
2. **Hour 2**: Implement location filtering and status updates
3. **Hour 3**: Add real-time refresh, modal dialogs, UX polish
4. **Hour 4**: Integration testing with Person 2

**Key Responsibilities:**
- Build responsive dashboard for emergency responders
- Implement location-based filtering (dropdown)
- Add status management (pending → assigned → resolved)
- Real-time auto-refresh every 30 seconds
- Mobile-friendly design

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Google Gemini API key (free tier available)
- Internet connection

---

### Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

---

### Step 2: Set Up Environment

**Windows PowerShell:**
```powershell
cd D:\crisis_resource_matching
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
$env:GEMINI_API_KEY = "your-api-key-here"
```

**Windows CMD:**
```cmd
cd D:\crisis_resource_matching
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
cd /path/to/crisis_resource_matching
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your-api-key-here"
```

---

### Step 3: Process Test Messages

```bash
python process_messages.py
```

This will:
- Load emergency messages from `data/emergency_messages.txt`
- Process each with Gemini AI
- Calculate priority scores
- Store in `data/messages_db.json`

Expected output:
```
PROCESSING MESSAGES WITH AI
============================================================

[1/10] Processing: Need food urgently near Tambaram...
  ✓ Need: food | Location: Tambaram
  ✓ Priority: HIGH (68.5/100)

...

🎉 SUCCESS! Database populated with processed messages
```

---

### Step 4: Launch Web Dashboard

```bash
python app.py
```

Output:
```
============================================================
🚨 CRISIS MANAGEMENT AI SYSTEM
============================================================

📍 Dashboard URL: http://localhost:5000

⚠️  Make sure to set GEMINI_API_KEY environment variable!
============================================================

 * Running on http://0.0.0.0:5000
```

---

### Step 5: Access Dashboard

Open browser to: **http://localhost:5000**

You'll see:
- **Statistics Cards**: Critical/High/Medium/Low counts
- **Location Filter**: Dropdown to filter by area
- **Status Filter**: Pending/Assigned/Resolved
- **Message Cards**: Sorted by priority (highest first)
- **Submit Button**: Add new emergency messages

---

## 📂 Project Structure

```
crisis_resource_matching/
│
├── config.py                    # Configuration settings
├── ai_processor.py              # Gemini AI integration (PERSON 1)
├── priority_engine.py           # Time-aware scoring (PERSON 1)
├── database.py                  # JSON storage (PERSON 1)
├── app.py                       # Flask web app (PERSON 2)
├── process_messages.py          # Demo script (BOTH)
├── requirements.txt             # Dependencies
├── README.md                    # This file
│
├── data/
│   ├── emergency_messages.txt   # Input messages
│   ├── resources.py             # Available resources
│   └── messages_db.json         # Processed messages (auto-generated)
│
├── templates/
│   └── dashboard.html           # Frontend UI (PERSON 2)
│
└── static/
    ├── style.css                # Styling (PERSON 2)
    └── script.js                # JavaScript (PERSON 2)
```

---

## 🎯 Testing Checklist

### Backend Tests (Person 1)
- [ ] AI processor correctly extracts need type
- [ ] Location detection works for all areas
- [ ] Urgency scoring is accurate (1-10 scale)
- [ ] Vulnerable group detection (children, elderly)
- [ ] Fallback analysis works without API key
- [ ] Time-based priority boost (nighttime shelter)
- [ ] Database stores and retrieves correctly

### Frontend Tests (Person 2)
- [ ] Dashboard loads without errors
- [ ] Location filter updates message list
- [ ] Status filter works (pending/assigned/resolved)
- [ ] Message cards display all information
- [ ] Modal dialogs open and close
- [ ] Submit new message works
- [ ] Statistics update correctly
- [ ] Mobile responsive design
- [ ] Auto-refresh every 30 seconds

---

## 🔥 Time-Sensitive Prioritization Examples

### Example 1: Nighttime Shelter (CRITICAL Priority Boost)
**Message:** *"Family of 4 with children needs shelter after flood in Tambaram"*  
**Time:** 9:00 PM (21:00)  
**Result:** Priority score increased by 25 points  
**Reason:** Nighttime exposure (6 PM - 6 AM) is life-threatening

### Example 2: Medical Emergency (Always CRITICAL)
**Message:** *"Elderly person having chest pain in Velachery"*  
**Time:** Any time  
**Result:** Always marked HIGH/CRITICAL  
**Reason:** Medical emergencies require immediate attention

### Example 3: Meal Time Food Request
**Message:** *"No food for children since yesterday in Perungudi"*  
**Time:** 1:00 PM (13:00)  
**Result:** Priority boost during meal hours  
**Reason:** Peak meal time (12-2 PM) for vulnerable populations

---

## 🛠️ Customization Tips

### Add New Locations
Edit `config.py`:
```python
LOCATIONS = ["Tambaram", "Velachery", "Perungudi", "Saidapet", "YourCity", "Other"]
```

### Adjust Priority Weights
Edit `priority_engine.py`:
```python
self.weights = {
    "base_urgency": 0.30,        # Change these values
    "time_sensitivity": 0.25,    # Total must equal 1.0
    "vulnerable_groups": 0.20,
    "immediate_danger": 0.15,
    "people_count": 0.10
}
```

### Change Time-Sensitive Hours
Edit `config.py`:
```python
TIME_SENSITIVE_NEEDS = {
    "shelter": {
        "critical_hours": list(range(18, 24)) + list(range(0, 6)),  # 6 PM - 6 AM
        "reason": "Nighttime exposure is life-threatening"
    }
}
```

---

## 🐛 Troubleshooting

### Issue: "AI processor not initialized"
**Solution:** Set GEMINI_API_KEY environment variable
```powershell
$env:GEMINI_API_KEY = "your-key-here"
```

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:** Change port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Issue: "No messages showing in dashboard"
**Solution:** Run `process_messages.py` first to populate database

### Issue: "API rate limit exceeded"
**Solution:** Gemini free tier has limits. Wait a few minutes or use fallback mode.

---

## 📊 API Endpoints Reference

### GET `/api/messages`
Query params: `?location=Tambaram&status=pending`  
Returns: List of filtered messages

### GET `/api/statistics`
Returns: Summary stats (counts by urgency, location, status)

### POST `/api/submit_message`
Body: `{"message": "Emergency text here"}`  
Returns: Processed message with AI analysis and priority

### POST `/api/update_status`
Body: `{"message_id": 1, "status": "assigned", "assigned_to": "Team A"}`  
Returns: Success confirmation

### POST `/api/process_bulk`
Body: `{"messages": ["msg1", "msg2", ...]}`  
Returns: Bulk processing results

---

## 🏆 Hackathon Presentation Tips

### Demo Flow (5 minutes)
1. **Show Problem** (30 sec): Display unstructured emergency messages
2. **Show AI Analysis** (1 min): Run process_messages.py, explain AI extraction
3. **Show Dashboard** (2 min): Filter by location, show priority ranking
4. **Show Time Sensitivity** (1 min): Explain nighttime shelter prioritization
5. **Submit New Message** (30 sec): Live demo of submitting and processing

### Key Talking Points
- "AI understands context, not just keywords"
- "Time-aware: nighttime shelter = higher priority"
- "Detects vulnerable populations automatically"
- "Location-based filtering for responder teams"
- "Real-time dashboard, auto-refreshes"

### Impressive Features to Highlight
- Gemini AI integration (cutting-edge)
- Multi-factor priority scoring (not just simple ranking)
- Time-based urgency adjustments
- Fallback mode if AI fails (reliability)
- Mobile-responsive UI

---

## 📈 Future Enhancements (Post-Hackathon)

- [ ] SMS integration (Twilio API)
- [ ] WhatsApp/Twitter monitoring
- [ ] Map view with geolocation
- [ ] Resource allocation automation
- [ ] Historical analytics
- [ ] Multi-language support
- [ ] Push notifications for responders
- [ ] Voice message transcription

---

## 📝 License

MIT License - Free to use for hackathons and educational purposes

---

## 🙏 Credits

Built for disaster relief and emergency response hackathon

**Technologies Used:**
- Google Gemini AI (LLM)
- Flask (Web Framework)
- Python 3.8+
- Vanilla JavaScript (No React/Vue complexity)

---

## 📞 Support During Hackathon

If you encounter issues during the hackathon:

1. Check this README troubleshooting section
2. Review terminal error messages
3. Test with `python process_messages.py` first
4. Verify API key is set correctly
5. Check browser console for frontend errors (F12)

---

**Good luck with your hackathon! 🚀**

**Remember:** The goal is to save lives by helping responders prioritize emergencies effectively!
