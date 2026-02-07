"""
WORK DIVISION GUIDE - Crisis Management AI System
For 2-person team working in parallel for 6 hours
"""

print("""
╔════════════════════════════════════════════════════════════════════╗
║          CRISIS MANAGEMENT AI SYSTEM - WORK DIVISION               ║
║                    6-Hour Hackathon Timeline                       ║
╚════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────┐
│ 🔵 PERSON 1: AI BACKEND DEVELOPER                                  │
└────────────────────────────────────────────────────────────────────┘

📁 FILES TO WORK ON:
  • ai_processor.py         - Gemini AI integration
  • priority_engine.py      - Scoring logic
  • database.py             - Data storage
  • config.py               - Configuration
  • process_messages.py     - Testing

⏰ TIMELINE:

HOUR 0-1: Setup & Testing
  ✓ Get Gemini API key from https://makersuite.google.com/app/apikey
  ✓ Install dependencies: pip install -r requirements.txt
  ✓ Set API key: $env:GEMINI_API_KEY = "your-key"
  ✓ Test AI processor: Run ai_processor.py directly
  ✓ Verify message analysis works
  
HOUR 1-2: Fine-tune AI Analysis
  ✓ Test with various message types
  ✓ Adjust fallback logic in ai_processor.py
  ✓ Ensure location detection works
  ✓ Test vulnerable group detection
  ✓ Handle edge cases (unclear messages)
  
HOUR 2-3: Priority Engine Optimization
  ✓ Adjust time-sensitive hours in config.py
  ✓ Test nighttime shelter prioritization
  ✓ Tune priority weights in priority_engine.py
  ✓ Verify scoring makes sense
  ✓ Run process_messages.py to see results
  
HOUR 3-4: Integration & Testing
  ✓ Coordinate with Person 2
  ✓ Test full pipeline (message → AI → priority → DB)
  ✓ Fix any bugs in AI analysis
  ✓ Optimize API calls (rate limiting)
  ✓ Prepare demo messages

HOUR 4-5: Polish & Demo Prep
  ✓ Add more test messages
  ✓ Document AI behavior
  ✓ Test fallback mode (without API)
  ✓ Prepare presentation points
  
HOUR 5-6: Final Testing & Presentation
  ✓ Full system integration test
  ✓ Practice demo flow
  ✓ Document key features
  ✓ Help with presentation

🎯 KEY RESPONSIBILITIES:
  • Ensure AI accurately extracts need, location, urgency
  • Implement time-aware prioritization (nighttime shelter boost)
  • Handle API errors gracefully with fallback
  • Test edge cases and unusual messages


┌────────────────────────────────────────────────────────────────────┐
│ 🟢 PERSON 2: FRONTEND/WEB DEVELOPER                                │
└────────────────────────────────────────────────────────────────────┘

📁 FILES TO WORK ON:
  • app.py                  - Flask web application
  • templates/dashboard.html - UI structure
  • static/style.css        - Styling
  • static/script.js        - Interactive features

⏰ TIMELINE:

HOUR 0-1: Setup & Basic UI
  ✓ Install Flask: pip install -r requirements.txt
  ✓ Run app.py to test basic setup
  ✓ Verify dashboard.html loads
  ✓ Test API endpoints with browser
  ✓ Check basic styling works
  
HOUR 1-2: Location Filtering
  ✓ Implement location dropdown in HTML
  ✓ Add JavaScript filter function
  ✓ Connect to /api/messages endpoint
  ✓ Test filtering by location
  ✓ Add status filtering (pending/assigned/resolved)
  
HOUR 2-3: Message Display & UX
  ✓ Style message cards (CSS)
  ✓ Add urgency color coding (CRITICAL=red, etc.)
  ✓ Implement message detail modal
  ✓ Add real-time statistics display
  ✓ Test responsive design (mobile/desktop)
  
HOUR 3-4: Interactive Features
  ✓ Add "Submit New Message" button/form
  ✓ Implement status update (pending → assigned → resolved)
  ✓ Add auto-refresh every 30 seconds
  ✓ Coordinate with Person 1 on API integration
  ✓ Test all interactive elements
  
HOUR 4-5: Polish & UX Improvements
  ✓ Add loading animations
  ✓ Improve mobile responsiveness
  ✓ Add tooltips/help text
  ✓ Test user flow
  ✓ Fix any UI bugs
  
HOUR 5-6: Final Testing & Presentation
  ✓ Full system integration test
  ✓ Test with live data from Person 1
  ✓ Prepare demo walkthrough
  ✓ Document UI features

🎯 KEY RESPONSIBILITIES:
  • Build responsive dashboard for emergency responders
  • Implement location-based filtering
  • Add status management (pending → assigned → resolved)
  • Real-time auto-refresh functionality
  • Mobile-friendly design


┌────────────────────────────────────────────────────────────────────┐
│ 🔄 COORDINATION POINTS (Both People)                               │
└────────────────────────────────────────────────────────────────────┘

After HOUR 1: Quick sync
  ✓ Person 1: Confirm AI is working
  ✓ Person 2: Confirm web app loads
  ✓ Run process_messages.py together
  
After HOUR 3: Integration checkpoint
  ✓ Test full pipeline together
  ✓ Submit message through UI
  ✓ Verify AI processes correctly
  ✓ Check priority ranking
  
After HOUR 5: Demo preparation
  ✓ Both: Prepare presentation
  ✓ Identify key features to highlight
  ✓ Prepare test messages for live demo
  ✓ Plan 5-minute demo flow


┌────────────────────────────────────────────────────────────────────┐
│ 🧪 TESTING CHECKLIST (Both collaborate)                            │
└────────────────────────────────────────────────────────────────────┘

Backend Tests (Person 1):
  □ AI correctly extracts need type
  □ Location detection works
  □ Urgency scoring is accurate
  □ Vulnerable group detection works
  □ Fallback works without API key
  □ Time-based priority boost functions
  □ Database stores/retrieves correctly
  
Frontend Tests (Person 2):
  □ Dashboard loads without errors
  □ Location filter updates messages
  □ Status filter works
  □ Message cards display info
  □ Modal dialogs work
  □ Submit new message functions
  □ Statistics update
  □ Mobile responsive
  □ Auto-refresh works
  
Integration Tests (Both):
  □ Submit message → AI analysis → Display
  □ Priority ranking is correct
  □ Location filtering accurate
  □ Status updates persist
  □ Real-time refresh works


┌────────────────────────────────────────────────────────────────────┐
│ 📋 DEMO PREPARATION (30 minutes before presentation)               │
└────────────────────────────────────────────────────────────────────┘

Person 1:
  • Prepare 5-10 demo messages (varied urgency)
  • Run process_messages.py to populate DB
  • Document AI features to highlight
  • Prepare to explain time-aware scoring
  
Person 2:
  • Polish UI for presentation
  • Test demo flow (filter, click, status update)
  • Prepare to explain responder workflow
  • Screenshot impressive features


┌────────────────────────────────────────────────────────────────────┐
│ 🎤 PRESENTATION FLOW (5 minutes)                                   │
└────────────────────────────────────────────────────────────────────┘

1. Problem Statement (30 sec)
   • Unstructured emergency messages
   • Manual processing is slow/error-prone
   
2. Our Solution (30 sec)
   • AI-powered interpretation (Gemini)
   • Time-aware prioritization
   
3. Live Demo (3 min)
   • Show dashboard with filtered messages
   • Explain priority ranking
   • Submit new message live
   • Show AI analysis
   • Demonstrate location filtering
   
4. Key Features (1 min)
   • Time-sensitive scoring (nighttime shelter)
   • Vulnerable population detection
   • Real-time responder dashboard
   
5. Q&A (remainder)


┌────────────────────────────────────────────────────────────────────┐
│ 🚨 EMERGENCY TROUBLESHOOTING                                       │
└────────────────────────────────────────────────────────────────────┘

If AI not working:
  → Use fallback mode (keyword-based)
  → System still functions!
  
If web UI crashes:
  → Restart Flask: python app.py
  → Check browser console (F12)
  
If demo breaks:
  → Have screenshots ready
  → Explain features verbally
  
If time runs out:
  → Focus on core features first
  → Skip polish, get functionality working


╔════════════════════════════════════════════════════════════════════╗
║  🎯 SUCCESS CRITERIA                                               ║
║  ✓ AI processes messages and extracts info                        ║
║  ✓ Priority ranking works (time-aware)                            ║
║  ✓ Web dashboard displays sorted messages                         ║
║  ✓ Location filtering functional                                  ║
║  ✓ Can submit new messages                                        ║
║  ✓ Demo runs smoothly                                             ║
╚════════════════════════════════════════════════════════════════════╝

Good luck! You've got this! 🚀
""")
